from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, TYPE_CHECKING
from app.db.session import Base

if TYPE_CHECKING:
    from .message_model import Message
    from .customer_model import Customer

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    thread_id: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String(50), default="web")
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    customer: Mapped["Customer"] = relationship("Customer")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation")
