from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from .base import BaseModel

class ConversationChannel(str, Enum):
    WEB = "web"
    WHATSAPP = "whatsapp"
    EMAIL = "email"

class ConversationStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"
    ESCALATED = "escalated"

class Conversation(BaseModel):
    __tablename__ = "conversations"

    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"), nullable=False)
    channel: Mapped[ConversationChannel] = mapped_column(Enum(ConversationChannel), nullable=False)
    status: Mapped[ConversationStatus] = mapped_column(Enum(ConversationStatus), default=ConversationStatus.OPEN, nullable=False)
    
    customer: Mapped["Customer"] = relationship("Customer", backref="conversations") # Establish relationship
    messages: Mapped[list["Message"]] = relationship("Message", backref="conversation", lazy="dynamic") # For fetching messages

    def __repr__(self):
        return f"<Conversation(customer_id={self.customer_id}, channel='{self.channel.value}', status='{self.status.value}')>"
