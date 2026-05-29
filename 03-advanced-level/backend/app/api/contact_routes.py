from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db, AsyncSessionLocal
from ..repositories.customer_repository import CustomerRepository
from ..services.chat_service import ChatService
from ..schemas.contact_schema import ContactForm, ContactResponse
import asyncio

router = APIRouter(prefix="/contact", tags=["Contact"])

async def process_contact_in_background(customer_id: int, message: str, email: str):
    async with AsyncSessionLocal() as db:
        chat_service = ChatService(db)
        # We use channel="email" to trigger the automatic email response in ChatService.process_chat
        async for _ in chat_service.process_chat(
            customer_id=customer_id,
            message_content=message,
            channel="email",
            recipient=email
        ):
            pass

@router.post("/", response_model=ContactResponse)
async def submit_contact_form(
    form: ContactForm, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    cust_repo = CustomerRepository(db)
    
    # 1. Get or Create Customer
    customer = await cust_repo.get_by_email(form.email)
    if not customer:
        customer = await cust_repo.create({
            "name": form.name,
            "email": form.email,
            "company": form.company
        })
    
    # 2. Add to background tasks so we can respond to the web request immediately
    background_tasks.add_task(process_contact_in_background, customer.id, form.message, form.email)
    
    return {
        "status": "success", 
        "message": "Your message has been received! Our AI agents are processing it and will reply to your email shortly."
    }
