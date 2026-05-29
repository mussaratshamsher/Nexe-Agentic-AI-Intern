from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..services.chat_service import ChatService
from ..repositories.customer_repository import CustomerRepository
from ..logs.execution_logger import ExecutionLogger
import re

router = APIRouter(tags=["Webhooks"])

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    # Check if the content type is form-urlencoded (Twilio) or JSON (Evolution API)
    content_type = request.headers.get("Content-Type", "")
    
    if "application/x-www-form-urlencoded" in content_type:
        # Twilio Webhook
        form_data = await request.form()
        phone = form_data.get("From", "").replace("whatsapp:", "")
        message_text = form_data.get("Body", "")
        
        if not message_text or not phone:
            return {"status": "empty message"}
            
        return await process_incoming_message(phone, message_text, db)
    else:
        # Evolution API / JSON
        data = await request.json()
        
        # Evolution API sends various event types
        event = data.get("event")
        if event != "messages.upsert":
            return {"status": "ignored"}

        msg_data = data.get("data", {})
        if not msg_data:
            return {"status": "no data"}

        # Extract info
        remote_jid = msg_data.get("key", {}).get("remoteJid", "")
        phone = remote_jid.split("@")[0]
        message_text = msg_data.get("message", {}).get("conversation", "") or \
                    msg_data.get("message", {}).get("extendedTextMessage", {}).get("text", "")
        
        if not message_text or not phone:
            return {"status": "empty message"}

        return await process_incoming_message(phone, message_text, db)

async def process_incoming_message(phone: str, message_text: str, db: AsyncSession):
    # Check if this is an admin approval reply
    # Format: "Approve 123" or "Approve 123 This is my edit"
    approval_match = re.match(r"Approve\s+(\d+)(.*)", message_text, re.IGNORECASE)
    if approval_match:
        # Verify if this phone is the admin phone
        from ..config.settings import settings
        admin_phone = "".join(filter(str.isdigit, settings.MY_PHONE_NUMBER or ""))
        if phone == admin_phone:
            pending_id = int(approval_match.group(1))
            edit = approval_match.group(2).strip() or None
            
            chat_service = ChatService(db)
            success = await chat_service.approve_response(pending_id, edit)
            return {"status": "approved" if success else "failed"}

    # Regular customer message
    # 1. Get or Create Customer
    cust_repo = CustomerRepository(db)
    customer = await cust_repo.get_by_email(f"{phone}@whatsapp.com") # Using phone as identifier
    if not customer:
        customer = await cust_repo.create({
            "name": f"WhatsApp User {phone[-4:]}",
            "email": f"{phone}@whatsapp.com",
            "company": "WhatsApp"
        })

    # 2. Process via ChatService
    chat_service = ChatService(db)
    # We use a wrapper because process_chat is a generator
    async for _ in chat_service.process_chat(
        customer_id=customer.id,
        message_content=message_text,
        channel="whatsapp",
        recipient=phone
    ):
        pass # The generator handles sending the message back

    return {"status": "processed"}
