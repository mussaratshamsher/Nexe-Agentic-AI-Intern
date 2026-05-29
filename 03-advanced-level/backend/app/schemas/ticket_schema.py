from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    customer_id: int
    priority: Optional[str] = "medium"
    issue_summary: str
    is_autopilot: Optional[int] = 0
    ai_draft: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_agent: Optional[str] = None
    issue_summary: Optional[str] = None
    is_autopilot: Optional[int] = None
    ai_draft: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    status: str
    assigned_agent: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
