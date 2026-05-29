import asyncio
from ..db.session import AsyncSessionLocal
from ..tools.gmail_tools import GmailService
from .chat_service import ChatService
from ..repositories.customer_repository import CustomerRepository
from ..repositories.conversation_repository import ConversationRepository
from ..logs.execution_logger import ExecutionLogger

class IngestionService:
    @staticmethod
    async def poll_gmail():
        """Polls Gmail for unread messages and processes them"""
        while True:
            try:
                messages = await GmailService.get_unread_messages()
                if messages:
                    # We need a new DB session for each poll iteration
                    async with AsyncSessionLocal() as db:

                        chat_service = ChatService(db)
                        cust_repo = CustomerRepository(db)
                        conv_repo = ConversationRepository(db)
                        
                        for msg in messages:
                            # 1. Check if thread already processed
                            existing_conv = await conv_repo.get_by_thread_id(msg['threadId'])
                            if existing_conv:
                                # Logic: We have a history, just append message to history
                                pass 
                            
                            await ExecutionLogger.log("Ingestion", f"Processing email from {msg['sender']}", msg['subject'])
                            
                            # 2. Get or Create Customer
                            email_addr = msg['sender'].split("<")[-1].replace(">", "").strip()
                            customer = await cust_repo.get_by_email(email_addr)
                            if not customer:
                                customer = await cust_repo.create({
                                    "name": msg['sender'].split("<")[0].strip() or email_addr,
                                    "email": email_addr,
                                    "company": "Email Inquiry"
                                })

                            # 3. Process via ChatService
                            async for _ in chat_service.process_chat(
                                customer_id=customer.id,
                                message_content=f"Subject: {msg['subject']}\n\n{msg['body']}",
                                channel="email",
                                recipient=email_addr,
                                thread_id=msg['threadId']
                            ):
                                pass
                            
                            # 4. Mark as read
                            await GmailService.mark_as_read(msg['id'])
                
            except Exception as e:
                await ExecutionLogger.log("Ingestion", "Error in Gmail polling", str(e))
            
            # Wait for 60 seconds before next poll
            await asyncio.sleep(60)

    @staticmethod
    def start_background_tasks():
        loop = asyncio.get_event_loop()
        loop.create_task(IngestionService.poll_gmail())
