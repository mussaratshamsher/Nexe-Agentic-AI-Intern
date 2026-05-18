from datetime import datetime
from typing import Optional, Any
from pydantic import Field
from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema

# Enum for task type, matching ORM Enum
class TaskTypeEnum(str):
    GENERAL = "general"
    SUPPORT_TICKET = "support_ticket"
    LEAD_QUALIFICATION = "lead_qualification"
    PROPOSAL_GENERATION = "proposal_generation"
    # Add more task types as needed

# Enum for task status, matching ORM Enum
class TaskStatusEnum(str):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskBase(BaseSchema):
    task_type: TaskTypeEnum
    assigned_agent_name: Optional[str] = None
    status: TaskStatusEnum
    result: Optional[Any] = None # Store result as dict or JSON string

class TaskCreate(BaseCreateSchema):
    task_type: TaskTypeEnum = Field(..., description="Type of task to be created")
    assigned_agent_name: Optional[str] = Field(None, description="Name of the agent assigned to this task")
    # Status is PENDING by default, result is None

class TaskUpdate(BaseUpdateSchema):
    assigned_agent_name: Optional[str] = None
    status: Optional[TaskStatusEnum] = None
    result: Optional[Any] = None

class TaskResponse(TaskBase): # Inherits common fields from TaskBase
    id: int
    created_at: datetime
