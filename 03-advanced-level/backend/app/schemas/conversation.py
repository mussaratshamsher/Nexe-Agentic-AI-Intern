from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema

# Enum for conversation channel, matching ORM Enum
class ConversationChannelEnum(str):
    WEB = "web"
    WHATSAPP = "whatsapp"
    EMAIL = "email"

# Enum for conversation status, matching ORM Enum
class ConversationStatusEnum(str):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"
    ESCALATED = "escalated"

class ConversationBase(BaseSchema):
    customer_id: int
    channel: ConversationChannelEnum
    status: ConversationStatusEnum

class ConversationCreate(BaseCreateSchema):
    customer_id: int = Field(..., description="ID of the customer associated with the conversation")
    channel: ConversationChannelEnum = Field(..., description="Channel through which the conversation occurred")
    # Status is typically set to OPEN by default, so not included in create payload

class ConversationUpdate(BaseUpdateSchema):
    status: Optional[ConversationStatusEnum] = None
    # Fields like customer_id, channel, and created_at are generally not updated

class ConversationResponse(ConversationBase): # Inherits common fields from ConversationBase
    id: int
    created_at: datetime

# Schema for message, to be nested or referenced
class MessageBase(BaseModel):
    sender_type: str # Should be an Enum, but keep as str for now, will map later
    content: str
    timestamp: datetime

class MessageCreate(BaseModel): # For sending a new message
    content: str = Field(..., description="The content of the message")

class MessageResponse(MessageBase): # For receiving messages
    id: int
    conversation_id: int
    sender_type: str # e.g., "user", "agent", "system"
    content: str
    timestamp: datetime

class ConversationDetailResponse(ConversationResponse):
    # Embed messages within the conversation response
    messages: List[MessageResponse] = []
