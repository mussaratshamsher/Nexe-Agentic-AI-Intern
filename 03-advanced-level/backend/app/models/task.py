from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, Any

from .base import BaseModel

class TaskType(str, Enum):
    GENERAL = "general"
    SUPPORT_TICKET = "support_ticket"
    LEAD_QUALIFICATION = "lead_qualification"
    PROPOSAL_GENERATION = "proposal_generation"
    # Add more task types as needed

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Task(BaseModel):
    __tablename__ = "tasks"

    task_type: Mapped[TaskType] = mapped_column(Enum(TaskType), nullable=False)
    assigned_agent_name: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Name of agent assigned, e.g., "Sales Agent"
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    result: Mapped[Optional[str]] = mapped_column(String, nullable=True) # JSON or text result of the task
    # created_at is inherited from BaseModel

    def __repr__(self):
        return f"<Task(type='{self.task_type.value}', status='{self.status.value}', assigned_agent='{self.assigned_agent_name}')>"
