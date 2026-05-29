from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.customer_schema import CustomerResponse, CustomerCreate, CustomerUpdate
from ..core.dependencies import get_customer_repo, get_current_user
from ..models.user_model import User

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    customer_repo = Depends(get_customer_repo),
    current_user: User = Depends(get_current_user)
):
    return await customer_repo.get_all(skip, limit)

@router.get("/{id}", response_model=CustomerResponse)
async def get_customer(
    id: int,
    customer_repo = Depends(get_customer_repo),
    current_user: User = Depends(get_current_user)
):
    customer = await customer_repo.get_by_id(id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer_in: CustomerCreate,
    customer_repo = Depends(get_customer_repo),
    current_user: User = Depends(get_current_user)
):
    return await customer_repo.create(customer_in)
