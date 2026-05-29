from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class KnowledgeBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None

class KnowledgeCreate(KnowledgeBase):
    pass

class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None

class KnowledgeResponse(KnowledgeBase):
    id: int
    last_used: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
