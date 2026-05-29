from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.conversation_model import Conversation
from typing import Optional

class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_thread_id(self, thread_id: str) -> Optional[Conversation]:
        result = await self.db.execute(select(Conversation).where(Conversation.thread_id == thread_id))
        return result.scalars().first()

    async def create(self, customer_id: int, channel: str, thread_id: str = None) -> Conversation:
        conv = Conversation(customer_id=customer_id, channel=channel, thread_id=thread_id)
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return conv
