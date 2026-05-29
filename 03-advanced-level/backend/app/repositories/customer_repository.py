from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate
from typing import Optional, List

class CustomerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        result = await self.db.execute(select(Customer).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        result = await self.db.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[Customer]:
        result = await self.db.execute(select(Customer).where(Customer.email == email))
        return result.scalars().first()

    async def create(self, customer_in: dict) -> Customer:
        db_customer = Customer(**customer_in)
        self.db.add(db_customer)
        await self.db.commit()
        await self.db.refresh(db_customer)
        return db_customer

    async def update(self, db_customer: Customer, customer_in: CustomerUpdate) -> Customer:
        update_data = customer_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        
        self.db.add(db_customer)
        await self.db.commit()
        await self.db.refresh(db_customer)
        return db_customer
