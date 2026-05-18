from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from .base import BaseModel

class LogStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"
    PENDING = "pending"

class ExecutionLog(BaseModel):
    __tablename__ = "execution_logs"

    agent_name: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False) # e.g., "lead_qualification", "create_ticket"
    status: Mapped[LogStatus] = mapped_column(Enum(LogStatus), nullable=False)
    details: Mapped[Optional[str]] = mapped_column(String, nullable=True) # JSON string or detailed text
    # created_at is inherited from BaseModel and used as timestamp

    def __repr__(self):
        return f"<ExecutionLog(agent='{self.agent_name}', action='{self.action}', status='{self.status.value}')>"
