from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.logs.logger import setup_logger
# Assume services are available or will be implemented
# from app.services.customer_service import CustomerService
# from app.services.ticket_service import TicketService

logger = setup_logger(__name__)

# --- Pydantic models for tool arguments ---
class CreateCustomerArgs(BaseModel):
    name: str = Field(..., description="Customer's full name")
    email: Optional[str] = Field(None, description="Customer's email address")
    phone: Optional[str] = Field(None, description="Customer's phone number")
    company: Optional[str] = Field(None, description="Customer's company name")

class GetCustomerHistoryArgs(BaseModel):
    customer_id: int = Field(..., description="The ID of the customer to retrieve history for")

class CreateTicketArgs(BaseModel):
    customer_id: int = Field(..., description="The ID of the customer to associate the ticket with")
    priority: str = Field("medium", description="Priority of the ticket (low, medium, high, urgent)")
    status: str = Field("open", description="Status of the ticket (open, in_progress, resolved, closed)")
    assigned_agent_id: Optional[int] = Field(None, description="The ID of the agent to assign the ticket to")
    subject: str = Field(..., description="Subject or title of the support ticket")
    description: str = Field(..., description="Detailed description of the issue")

class GetOpenTicketsArgs(BaseModel):
    agent_id: Optional[int] = Field(None, description="Filter tickets assigned to a specific agent ID")

# --- Tool implementations ---

# Mock services for demonstration
class MockCustomerService:
    async def create_customer(self, name: str, email: Optional[str] = None, phone: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f"Mock: Creating customer - Name: {name}, Email: {email}, Company: {company}")
        # Simulate returning a created customer object with an ID
        return {"id": 999, "name": name, "email": email, "phone": phone, "company": company, "created_at": "2023-10-27T10:00:00Z"}

    async def get_customer_history(self, customer_id: int) -> Dict[str, Any]:
        logger.info(f"Mock: Getting history for customer ID: {customer_id}")
        # Simulate returning history data
        return {"customer_id": customer_id, "conversations": [], "tickets": []}

class MockTicketService:
    async def create_ticket(self, customer_id: int, subject: str, description: str, priority: str="medium", status: str="open", assigned_agent_id: Optional[int]=None) -> Dict[str, Any]:
        logger.info(f"Mock: Creating ticket for customer {customer_id} - Subject: {subject}")
        # Simulate returning a created ticket object with an ID
        return {"id": 101, "customer_id": customer_id, "subject": subject, "description": description, "priority": priority, "status": status, "assigned_agent_id": assigned_agent_id, "created_at": "2023-10-27T10:05:00Z"}

    async def get_open_tickets(self, agent_id: Optional[int]=None) -> List[Dict[str, Any]]:
        logger.info(f"Mock: Getting open tickets (assigned to agent ID: {agent_id})")
        # Simulate returning a list of open tickets
        return [{"id": 101, "customer_id": 1, "subject": "Issue with order", "status": "open", "priority": "high"}]

# Instantiate mock services
customer_service = MockCustomerService()
ticket_service = MockTicketService()

@tool(args_schema=CreateCustomerArgs, tool_name="create_customer")
async def create_customer(name: str, email: Optional[str] = None, phone: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a new customer record in the CRM.
    Useful for onboarding new clients or when a new contact is identified.
    """
    return await customer_service.create_customer(name=name, email=email, phone=phone, company=company)

@tool(args_schema=GetCustomerHistoryArgs, tool_name="get_customer_history")
async def get_customer_history(customer_id: int) -> Dict[str, Any]:
    """
    Retrieves the interaction history (conversations, tickets) for a specific customer.
    Useful for understanding past interactions before engaging with a customer.
    """
    return await customer_service.get_customer_history(customer_id=customer_id)

@tool(args_schema=CreateTicketArgs, tool_name="create_ticket")
async def create_ticket(customer_id: int, subject: str, description: str, priority: str="medium", status: str="open", assigned_agent_id: Optional[int]=None) -> Dict[str, Any]:
    """
    Creates a new support ticket for a customer.
    Use this when a customer reports an issue that requires support.
    """
    return await ticket_service.create_ticket(customer_id=customer_id, subject=subject, description=description, priority=priority, status=status, assigned_agent_id=assigned_agent_id)

@tool(args_schema=GetOpenTicketsArgs, tool_name="get_open_tickets")
async def get_open_tickets(agent_id: Optional[int]=None) -> List[Dict[str, Any]]:
    """
    Retrieves a list of all open support tickets.
    Can be filtered by assigned agent ID.
    Useful for agents to see pending tasks or for management overview.
    """
    return await ticket_service.get_open_tickets(agent_id=agent_id)
