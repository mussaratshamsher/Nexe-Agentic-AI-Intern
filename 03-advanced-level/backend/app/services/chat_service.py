from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.ticket_repository import TicketRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.knowledge_repository import KnowledgeRepository
from app.agents.stage1_agents.orchestrator import OrchestratorAgent
from app.models.conversation_model import Conversation
from app.models.message_model import Message

from app.agents.stage1_agents.sales_agent import SalesAgent
from app.agents.stage1_agents.support_agent import SupportAgent
from app.agents.stage1_agents.pm_agent import PMAgent
from app.agents.stage1_agents.content_agent import ContentAgent
from app.services.intelligence_service import IntelligenceService
from app.models.pending_review_model import PendingReview
from app.tools.communication_tools import CommunicationTools
from app.tools.crm_tools import CRMTools
from app.tools.knowledge_tools import KnowledgeTools
import json

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ticket_repo = TicketRepository(db)
        self.exec_repo = ExecutionRepository(db)
        self.cust_repo = CustomerRepository(db)
        self.kb_repo = KnowledgeRepository(db)
        self.orchestrator = OrchestratorAgent()
        
        # Real-world tools with DB access
        self.crm_tools = CRMTools(db)
        self.kb_tools = KnowledgeTools(db)
        
        self.agents = {
            "Sales": SalesAgent(),
            "Support": SupportAgent(),
            "PM": PMAgent(),
            "Content": ContentAgent()
        }

    async def process_chat(self, customer_id: int, message_content: str, channel: str = "web", recipient: str = None, thread_id: str = None):
        from ..repositories.conversation_repository import ConversationRepository
        conv_repo = ConversationRepository(self.db)
        
        # 1. Redundancy Check
        recent_msgs = await self.db.execute(
            select(Message)
            .join(Conversation)
            .where(Conversation.customer_id == customer_id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        last_msg = recent_msgs.scalar_one_or_none()
        if last_msg and last_msg.content.strip().lower() == message_content.strip().lower():
            return

        # 2. Relevancy Filter (Business/Job check)
        keywords = ["job", "business", "service", "inquiry", "work", "apply", "support", "help", "price", "plan"]
        if not any(k in message_content.lower() for k in keywords):
            yield "I am an AI business assistant. Please ask about business, jobs, or our services."
            return

        # 0. Analyze Sentiment (using 8B model)
        sentiment_data = await IntelligenceService.analyze_sentiment(message_content)

        # 1. Create/Retrieve Conversation
        conversation = None
        history_str = ""
        if thread_id:
            conversation = await conv_repo.get_by_thread_id(thread_id)
            
        if not conversation:
            conversation = await conv_repo.create(customer_id, channel, thread_id)
        else:
            for msg in conversation.messages[-5:]:
                history_str += f"{msg.sender_type}: {msg.content}\n"

        # 2. Store user message
        user_msg = Message(
            conversation_id=conversation.id, 
            sender_type="customer", 
            content=message_content,
            sentiment=sentiment_data['sentiment'],
            sentiment_score=sentiment_data['score']
        )
        self.db.add(user_msg)
        await self.db.commit()

        # --- RAG: Fetch relevant knowledge and CRM data before planning ---
        kb_context = await self.kb_tools.search_knowledge_base(message_content)
        customer = await self.cust_repo.get_by_id(customer_id)
        crm_history = await self.crm_tools.get_customer_history(customer.email) if customer else []
        
        enriched_context = {
            "knowledge": kb_context,
            "customer_profile": {
                "name": customer.name if customer else "Unknown",
                "email": customer.email if customer else "Unknown",
                "lead_score": customer.lead_score if customer else 0,
                "history": crm_history
            }
        }

        # 3. Trigger Orchestrator for Planning
        plan_data = await self.orchestrator.analyze_and_plan(
            message_content, 
            channel, 
            self.exec_repo, 
            history=history_str,
            context=enriched_context
        )
        is_sensitive = plan_data.get('is_sensitive', False)

        # 4. Execute delegated tasks
        outputs = []
        plan_steps = plan_data.get('plan', [])
        if not isinstance(plan_steps, list):
            plan_steps = []
            
        for step in plan_steps:
            if not isinstance(step, dict):
                continue
                
            agent_name = step.get('agent')
            task_desc = step.get('task')
            reasoning = step.get('reasoning', "")
            step_num = step.get('step_number', 1)
            
            if not agent_name or not task_desc:
                continue
                
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                # Pass enriched context to agents
                output = await agent.run(task_desc, context=enriched_context, repo=self.exec_repo)
                
                # Special Action: If Support Agent wants to create a ticket
                if agent_name == "Support" and "create ticket" in task_desc.lower():
                    ticket_res = await self.crm_tools.create_ticket(customer_id, task_desc)
                    output += f"\n[System: Ticket #{ticket_res['ticket_id']} created with {ticket_res['priority']} priority]"

                await self.exec_repo.log_action(
                    agent_name=agent_name,
                    action=f"Completed: {task_desc[:50]}...",
                    status="success",
                    details=output[:100],
                    reasoning=reasoning,
                    step_number=step_num
                )
                outputs.append({"agent": agent_name, "output": output})

        # 5. Yield Metadata
        metadata = {
            "conversation_id": conversation.id,
            "sentiment": sentiment_data['sentiment'],
            "sentiment_score": sentiment_data['score'],
            "strategic_reasoning": plan_data.get('strategic_reasoning', ""),
            "is_sensitive": is_sensitive
        }
        yield json.dumps(metadata) + "|||"

        # 6. Stream final response
        full_response = ""
        async for token in self.orchestrator.synthesize(
            message_content, 
            outputs, 
            channel, 
            plan_data.get('channel_guidelines', ""),
            self.exec_repo,
            history=history_str
        ):
            full_response += token
            if not is_sensitive:
                yield token

        if is_sensitive:
            pending = PendingReview(
                conversation_id=conversation.id,
                channel=channel,
                recipient_identifier=recipient or "Unknown",
                original_request=message_content,
                proposed_response=full_response,
                review_reason=plan_data.get('review_reason', "Unknown"),
                thread_id=thread_id
            )
            self.db.add(pending)
            await self.db.commit()
            
            admin_msg = f"🔍 Review Needed ({channel}):\nCustomer: {recipient or 'Unknown'}\nReason: {plan_data.get('review_reason')}\nProposed: {full_response[:100]}...\nReply 'Approve {pending.id}' to send."
            await CommunicationTools.notify_admin(admin_msg)
            yield "⚠️ Your request involves sensitive information and is being reviewed by our team. We will get back to you shortly."
            full_response = "Notice: Sensitive request under review."
        else:
            if channel == "email" and recipient:
                await CommunicationTools.send_email(recipient, "Re: Your Inquiry", full_response, thread_id=thread_id)
            elif channel == "whatsapp" and recipient:
                await CommunicationTools.send_whatsapp_message(recipient, full_response)

        # 7. Store AI response
        ai_msg = Message(conversation_id=conversation.id, sender_type="agent", content=full_response)
        self.db.add(ai_msg)
        
        # 8. Update Lead Score (Async using 8B model)
        if customer:
            lead_data = await IntelligenceService.calculate_lead_score(
                {"name": customer.name, "company": customer.company, "history": crm_history},
                [{"role": "user", "content": message_content}]
            )
            customer.lead_score = lead_data['score']
            customer.lead_status = lead_data['status']
            self.db.add(customer)

        await self.db.commit()

    async def approve_response(self, pending_id: int, edit: str = None):
        """Approves a pending response and sends it to the customer"""
        from sqlalchemy import select
        result = await self.db.execute(select(PendingReview).where(PendingReview.id == pending_id))
        pending = result.scalar_one_or_none()
        
        if not pending or pending.status != "pending":
            return False

        final_content = edit if edit else pending.proposed_response
        
        # Send via appropriate channel
        success = False
        if pending.channel == "email":
            success = await CommunicationTools.send_email(
                pending.recipient_identifier, 
                "Re: Your inquiry", 
                final_content,
                thread_id=pending.thread_id
            )
        elif pending.channel == "whatsapp":
            success = await CommunicationTools.send_whatsapp_message(
                pending.recipient_identifier, 
                final_content
            )
        else:
            # For web, we might just mark it as approved for the UI to show
            success = True

        if success:
            pending.status = "approved"
            pending.proposed_response = final_content
            # Log the message in the conversation
            ai_msg = Message(conversation_id=pending.conversation_id, sender_type="agent", content=final_content)
            self.db.add(ai_msg)
            await self.db.commit()
            
        return success
