from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.ticket_schema import TicketResponse, TicketCreate, TicketUpdate
from ..core.dependencies import get_ticket_repo, get_current_user
from ..models.user_model import User

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
    skip: int = 0,
    limit: int = 100,
    ticket_repo = Depends(get_ticket_repo),
    current_user: User = Depends(get_current_user)
):
    return await ticket_repo.get_all(skip, limit)

@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket_in: TicketCreate,
    ticket_repo = Depends(get_ticket_repo),
    current_user: User = Depends(get_current_user)
):
    return await ticket_repo.create(ticket_in)

@router.patch("/{id}", response_model=TicketResponse)
async def update_ticket(
    id: int,
    ticket_in: TicketUpdate,
    ticket_repo = Depends(get_ticket_repo),
    current_user: User = Depends(get_current_user)
):
    db_ticket = await ticket_repo.get_by_id(id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return await ticket_repo.update(db_ticket, ticket_in)
