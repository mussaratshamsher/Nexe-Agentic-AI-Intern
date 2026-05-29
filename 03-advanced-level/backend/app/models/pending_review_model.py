from sqlalchemy import String, Text, DateTime, func, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..db.session import Base

class PendingReview(Base):
    __tablename__ = "pending_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id"))
    channel: Mapped[str] = mapped_column(String(50))
    recipient_identifier: Mapped[str] = mapped_column(String(255)) # email or phone
    original_request: Mapped[str] = mapped_column(Text)
    proposed_response: Mapped[str] = mapped_column(Text)
    review_reason: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending") # pending, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    thread_id: Mapped[str] = mapped_column(String(255), nullable=True) # For Gmail threads
