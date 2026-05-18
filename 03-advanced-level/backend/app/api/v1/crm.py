from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.db.session import get_db_session
from app.schemas.crm import CustomerCreate, CustomerResponse, TicketCreate, TicketResponse # Define these schemas later
from app.models.customer import Customer # Import ORM models
from app.models.ticket import Ticket
from app.core.exceptions import NotFoundException, BadRequestException
from app.logs.logger import setup_logger

# Assume services are implemented and injected or available globally
# from app.services.customer_service import CustomerService
# from app.services.ticket_service import TicketService

logger = setup_logger(__name__)
crm_router = APIRouter()

# Mock services for now
class MockCustomerService:
    async def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Mock CRM: Creating customer: {customer_data['name']}")
        # Simulate returning a created customer object with an ID
        return {"id": 1001, **customer_data, "created_at": datetime.utcnow().isoformat()}

    async def get_customer_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        logger.info(f"Mock CRM: Getting customer by ID: {customer_id}")
        if customer_id == 1001:
            return {"id": 1001, "name": "Acme Corp", "email": "contact@acme.com", "phone": "123-456-7890", "company": "Acme Corp", "created_at": datetime.utcnow().isoformat()}
        return None
    
    async def get_all_customers(self) -> List[Dict[str, Any]]:
        logger.info("Mock CRM: Getting all customers")
        return [{"id": 1001, "name": "Acme Corp", "email": "contact@acme.com", "company": "Acme Corp", "created_at": datetime.utcnow().isoformat()}]

class MockTicketService:
    async def create_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Mock CRM: Creating ticket for customer ID: {ticket_data['customer_id']}")
        # Simulate returning a created ticket object with an ID
        return {"id": 2001, **ticket_data, "created_at": datetime.utcnow().isoformat(), "status": "open"}

    async def get_tickets_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        logger.info(f"Mock CRM: Getting tickets for customer ID: {customer_id}")
        # Simulate returning tickets
        return [{"id": 2001, "customer_id": customer_id, "subject": "Initial Inquiry", "description": "User has an initial inquiry.", "priority": "medium", "status": "open", "created_at": datetime.utcnow().isoformat()}]

customer_service = MockCustomerService()
ticket_service = MockTicketService()

# --- Customer Endpoints ---
@crm_router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_new_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db_session) # We'll use mock services for now, but DB is there for future
):
    """
    Creates a new customer in the CRM.
    """
    logger.info(f"API: POST /crm/customers - Creating customer: {customer_data.name}")
    # In a real app, this would use a repository/service with DB access.
    created_customer = await customer_service.create_customer(customer_data.model_dump())
    return CustomerResponse(**created_customer)

@crm_router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer_by_id(customer_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Retrieves a specific customer by their ID.
    """
    logger.info(f"API: GET /crm/customers/{customer_id}")
    customer = await customer_service.get_customer_by_id(customer_id)
    if customer is None:
        raise NotFoundException(detail=f"Customer with id {customer_id} not found")
    return CustomerResponse(**customer)

@crm_router.get("/customers", response_model=List[CustomerResponse])
async def list_customers(db: AsyncSession = Depends(get_db_session)):
    """
    Retrieves a list of all customers.
    """
    logger.info("API: GET /crm/customers - Listing all customers")
    customers = await customer_service.get_all_customers()
    return [CustomerResponse(**c) for c in customers]

# --- Ticket Endpoints ---
@crm_router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_new_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Creates a new support ticket.
    """
    logger.info(f"API: POST /crm/tickets - Creating ticket for customer ID: {ticket_data.customer_id}")
    created_ticket = await ticket_service.create_ticket(ticket_data.model_dump())
    return TicketResponse(**created_ticket)

@crm_router.get("/tickets/customer/{customer_id}", response_model=List[TicketResponse])
async def get_customer_tickets(customer_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Retrieves all tickets for a specific customer.
    """
    logger.info(f"API: GET /crm/tickets/customer/{customer_id}")
    tickets = await ticket_service.get_tickets_by_customer(customer_id)
    return [TicketResponse(**t) for t in tickets]

# Define necessary Pydantic schemas for CRM API (will be in schemas/crm.py)
# For now, defining them inline for clarity.
class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

class TicketBase(BaseModel):
    customer_id: int
    subject: str
    description: str
    priority: str = "medium"
    status: str = "open"
    assigned_agent_id: Optional[int] = None

class TicketCreate(TicketBase):
    pass

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
