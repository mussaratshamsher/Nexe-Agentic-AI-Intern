from datetime import datetime
from typing import Optional
from pydantic import Field
from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema

# Enum for ticket status, matching ORM Enum
class TicketStatusEnum(str):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"

# Enum for ticket priority, matching ORM Enum
class TicketPriorityEnum(str):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TicketBase(BaseSchema):
    customer_id: int
    priority: TicketPriorityEnum
    status: TicketStatusEnum
    assigned_agent_id: Optional[int] = None

class TicketCreate(BaseCreateSchema):
    customer_id: int = Field(..., description="ID of the customer associated with the ticket")
    priority: TicketPriorityEnum = Field(TicketPriorityEnum.MEDIUM, description="Priority of the ticket")
    status: TicketStatusEnum = Field(TicketStatusEnum.OPEN, description="Current status of the ticket")
    assigned_agent_id: Optional[int] = Field(None, description="ID of the agent assigned to the ticket")

class TicketUpdate(BaseUpdateSchema):
    priority: Optional[TicketPriorityEnum] = None
    status: Optional[TicketStatusEnum] = None
    assigned_agent_id: Optional[int] = None # Allow reassigning

class TicketResponse(TicketBase): # Inherits common fields from TicketBase
    id: int
    created_at: datetime
