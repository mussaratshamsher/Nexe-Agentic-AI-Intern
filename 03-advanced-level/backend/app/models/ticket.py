from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from .base import BaseModel

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Ticket(BaseModel):
    __tablename__ = "tickets"

    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"), nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    assigned_agent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True) # FK to users table for agent

    customer: Mapped["Customer"] = relationship("Customer", backref="tickets") # Establish relationship
    assigned_agent: Mapped[Optional["User"]] = relationship("User", backref="assigned_tickets") # Link to the assigned agent

    def __repr__(self):
        return f"<Ticket(customer_id={self.customer_id}, status='{self.status.value}', priority='{self.priority.value}', assigned_agent_id={self.assigned_agent_id})>"
