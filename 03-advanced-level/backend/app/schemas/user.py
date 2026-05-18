from typing import Optional
from pydantic import EmailStr
from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema

# Enum for user roles, matching the ORM Enum
class UserRoleEnum(str):
    ADMIN = "admin"
    USER = "user"
    AGENT = "agent" # For AI agents

class UserBase(BaseSchema):
    email: EmailStr
    role: UserRoleEnum

class UserCreate(BaseCreateSchema):
    email: EmailStr
    password: str # Plain text password for creation, will be hashed server-side
    role: Optional[UserRoleEnum] = UserRoleEnum.USER

class UserUpdate(BaseUpdateSchema):
    email: Optional[EmailStr] = None
    role: Optional[UserRoleEnum] = None
    # Password update should be handled via a separate endpoint for security

class UserInDB(UserBase): # Schema for data retrieved from DB
    hashed_password: str

class UserResponse(UserBase): # Schema for API response
    id: int
    created_at: datetime
