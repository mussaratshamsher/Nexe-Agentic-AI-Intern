from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..db.session import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_type: Mapped[str] = mapped_column(String(100), nullable=False)
    assigned_agent: Mapped[str] = mapped_column(String(100), nullable=False)
    task_status: Mapped[str] = mapped_column(String(50), default="pending")
    result: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
