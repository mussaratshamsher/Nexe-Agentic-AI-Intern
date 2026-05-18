from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Column, Integer, DateTime, func

# Base for declarative models
# AsyncAttrs allows us to use async methods with models (e.g., for session interaction)
Base = declarative_base(cls=AsyncAttrs)

class BaseModel(Base):
    __abstract__ = True # This model won't be mapped to a table, it's for inheritance

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        # Generic representation for debugging
        return f"<{self.__class__.__name__}(id={self.id})>"
