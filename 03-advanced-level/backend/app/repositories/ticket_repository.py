from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket_model import Ticket
from app.schemas.ticket_schema import TicketCreate, TicketUpdate
from typing import List, Optional

class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, ticket_in: TicketCreate) -> Ticket:
        db_ticket = Ticket(**ticket_in.model_dump(), status="open")
        self.db.add(db_ticket)
        await self.db.commit()
        await self.db.refresh(db_ticket)
        return db_ticket

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Ticket]:
        result = await self.db.execute(select(Ticket).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalars().first()

    async def update(self, db_ticket: Ticket, ticket_in: TicketUpdate) -> Ticket:
        update_data = ticket_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ticket, field, value)
        
        self.db.add(db_ticket)
        await self.db.commit()
        await self.db.refresh(db_ticket)
        return db_ticket
