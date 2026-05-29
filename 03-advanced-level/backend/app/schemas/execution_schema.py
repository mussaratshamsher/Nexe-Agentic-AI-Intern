from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ExecutionLogBase(BaseModel):
    agent_name: str
    action: str
    status: str = "info"
    details: Optional[str] = None
    reasoning: Optional[str] = None
    step_number: int = 1

class ExecutionLogCreate(ExecutionLogBase):
    pass

class ExecutionLogResponse(ExecutionLogBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
