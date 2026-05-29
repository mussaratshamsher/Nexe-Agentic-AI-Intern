from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chat_schema import ChatRequest, ConversationResponse
from app.services.chat_service import ChatService
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def send_message(chat_in: ChatRequest, db: AsyncSession = Depends(get_db)):
    service = ChatService(db)
    return StreamingResponse(
        service.process_chat(chat_in.customer_id, chat_in.message, chat_in.channel),
        media_type="text/event-stream"
    )
