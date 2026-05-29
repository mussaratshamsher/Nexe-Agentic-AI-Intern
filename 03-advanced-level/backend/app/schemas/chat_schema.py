from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    sender_type: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[int] = None

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    customer_id: int
    channel: str
    status: str
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    customer_id: int
    message: str
    channel: Optional[str] = "web"
