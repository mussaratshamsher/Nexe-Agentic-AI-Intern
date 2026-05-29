from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from ..models.message_model import Message
from ..models.conversation_model import Conversation
from ..schemas.chat_schema import MessageCreate, ConversationCreate

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, conv_in: ConversationCreate) -> Conversation:
        db_conv = Conversation(**conv_in.model_dump())
        self.db.add(db_conv)
        self.db.commit()
        self.db.refresh(db_conv)
        return db_conv

    def get_conversation(self, conv_id: int) -> Conversation:
        query = select(Conversation).where(Conversation.id == conv_id)
        result = self.db.execute(query)
        return result.scalars().first()

    def get_active_conversation_by_customer(self, customer_id: int) -> Conversation:
        query = select(Conversation).where(
            Conversation.customer_id == customer_id, 
            Conversation.status == "active"
        ).order_by(Conversation.created_at.desc())
        result = self.db.execute(query)
        return result.scalars().first()

    def create_message(self, msg_in: MessageCreate) -> Message:
        db_msg = Message(**msg_in.model_dump())
        self.db.add(db_msg)
        self.db.commit()
        self.db.refresh(db_msg)
        return db_msg

    def get_messages_by_conversation(self, conv_id: int) -> List[Message]:
        query = select(Message).where(Message.conversation_id == conv_id).order_by(Message.created_at.asc())
        result = self.db.execute(query)
        return result.scalars().all()
