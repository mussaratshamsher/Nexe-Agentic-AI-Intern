from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    id: str
    description: str
    assigned_to: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = []
    result: Optional[Any] = None
    created_at: datetime = Field(default_factory=datetime.now)

class AgentOutput(BaseModel):
    agent_name: str
    thought_process: str
    result: Any
    next_action: Optional[str] = None
    execution_time_ms: float

class ExecutionStep(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    agent_name: str
    action: str
    details: Optional[str] = None

class WorkflowResponse(BaseModel):
    workflow_id: str
    final_answer: str
    steps: List[ExecutionStep]
    metadata: Dict[str, Any] = {}
