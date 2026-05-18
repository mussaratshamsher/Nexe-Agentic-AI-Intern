from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from .base import BaseModel

class SenderType(str, Enum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system" # For automated messages or logs

class Message(BaseModel):
    __tablename__ = "messages"

    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_type: Mapped[SenderType] = mapped_column(Enum(SenderType), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    # timestamp is inherited from BaseModel and used as created_at

    def __repr__(self):
        return f"<Message(conversation_id={self.conversation_id}, sender_type='{self.sender_type.value}', content='{self.content[:50]}...')>"
