from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from .base import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    AGENT = "agent" # For AI agents

class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)

    # No created_at here as it's inherited from BaseModel
    # No id here as it's inherited from BaseModel

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role.value}')>"
