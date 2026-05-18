from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.db.session import get_db_session
from app.orchestration.orchestrator import OrchestrationManager # Assuming this will be injected
from app.schemas.chat import ChatMessageCreate, ChatResponse # Define these schemas later
from app.logs.logger import setup_logger

logger = setup_logger(__name__)
chat_router = APIRouter()

# Placeholder for orchestration manager dependency
# This would normally be defined in main.py or a core dependency file.
# For now, we'll use a mock that simulates its behavior.
class MockOrchestrationManager:
    async def process_message(self, user_input: str, conversation_id: int) -> Dict[str, Any]:
        logger.info(f"Mock OrchestrationManager: Processing message '{user_input}' for conversation {conversation_id}")
        # Simulate a response from the orchestrator
        return {"response": f"Mock response to: '{user_input}'"}

# Instantiate the mock manager for now. This will be replaced by the real one.
# In main.py, the real orchestration_manager will be initialized and provided.
mock_orchestration_manager = MockOrchestrationManager()

# Dummy get_orchestration_manager dependency for now
async def get_orchestration_manager_dependency():
    # This will be replaced by a real dependency that returns the singleton instance
    return mock_orchestration_manager

@chat_router.post("/message", response_model=ChatResponse)
async def handle_chat_message(
    message_data: ChatMessageCreate,
    # db: AsyncSession = Depends(get_db_session), # If DB is needed for history retrieval
    orchestrator: OrchestrationManager = Depends(get_orchestration_manager_dependency) # Use the dependency
):
    """
    Handles incoming chat messages from users.
    Activates the orchestration manager to process the message.
    """
    logger.info(f"API: POST /chat/message - Received message from user: {message_data.user_id} for conversation {message_data.conversation_id}")
    
    try:
        # Process the message through the orchestration manager
        response_data = await orchestrator.process_message(
            user_input=message_data.content,
            conversation_id=message_data.conversation_id
        )
        
        if "response" in response_data:
            logger.info(f"API: POST /chat/message - Successfully processed message. Sending response.")
            return ChatResponse(
                conversation_id=message_data.conversation_id,
                user_id=message_data.user_id,
                sender_type="agent", # Response comes from the system/agents
                content=response_data["response"],
                timestamp=datetime.utcnow()
            )
        else:
            logger.error(f"API: POST /chat/message - Orchestration manager returned an unexpected response: {response_data}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Orchestration manager failed to produce a valid response."
            )
            
    except Exception as e:
        logger.error(f"API: POST /chat/message - Error handling chat message for conversation {message_data.conversation_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the chat message: {str(e)}"
        )

# Define necessary Pydantic schemas for Chat API (will be in schemas/chat.py)
# For now, defining them inline for clarity, but should be moved to schemas/chat.py
class ChatMessageBase(BaseModel):
    conversation_id: int
    user_id: str # Identifier for the end-user
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatResponse(ChatMessageBase):
    sender_type: str # e.g., "user", "agent", "system"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
