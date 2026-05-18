from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from .base import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # created_at is inherited from BaseModel

    def __repr__(self):
        return f"<Customer(name='{self.name}', email='{self.email}', company='{self.company}')>"
