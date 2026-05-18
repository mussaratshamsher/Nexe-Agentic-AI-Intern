from datetime import datetime
from typing import Optional, Any
from pydantic import Field
from .base import BaseSchema, BaseCreateSchema

# Enum for log status, matching ORM Enum
class LogStatusEnum(str):
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"
    PENDING = "pending"

class ExecutionLogBase(BaseSchema):
    agent_name: str
    action: str
    status: LogStatusEnum
    details: Optional[Any] = None # Store details as dict or JSON string

class ExecutionLogCreate(BaseCreateSchema):
    agent_name: str = Field(..., description="Name of the agent performing the action")
    action: str = Field(..., description="Description of the action taken")
    status: LogStatusEnum = Field(..., description="Status of the action (success, failure, etc.)")
    details: Optional[Any] = Field(None, description="Detailed information about the action, e.g., parameters, results, error messages")

class ExecutionLogResponse(ExecutionLogBase): # Inherits common fields from ExecutionLogBase
    id: int
    created_at: datetime
