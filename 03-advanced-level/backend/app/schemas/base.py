from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    """Base Pydantic schema with common fields and configuration."""
    model_config = ConfigDict(from_attributes=True) # Allows ORM mapping

    id: int
    created_at: datetime

class BaseCreateSchema(BaseModel):
    """Base schema for creation payload, excluding auto-generated fields."""
    model_config = ConfigDict(from_attributes=True)
    pass # Placeholder, specific fields will be added by subclasses

class BaseUpdateSchema(BaseModel):
    """Base schema for update payload, excluding auto-generated fields."""
    model_config = ConfigDict(from_attributes=True)
    pass # Placeholder, specific fields will be added by subclasses
