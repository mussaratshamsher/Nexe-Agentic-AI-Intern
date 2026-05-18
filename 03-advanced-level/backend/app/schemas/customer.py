from typing import Optional
from pydantic import EmailStr, Field
from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema

class CustomerBase(BaseSchema):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class CustomerCreate(BaseCreateSchema):
    name: str = Field(..., min_length=1, description="Customer's full name")
    email: Optional[EmailStr] = Field(None, description="Customer's email address")
    phone: Optional[str] = Field(None, description="Customer's phone number")
    company: Optional[str] = Field(None, description="Customer's company name")

class CustomerUpdate(BaseUpdateSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class CustomerResponse(CustomerBase): # Inherits common fields from CustomerBase
    id: int
    created_at: datetime
