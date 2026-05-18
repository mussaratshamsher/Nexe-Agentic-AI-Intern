# This file will aggregate all API route routers for version 1.
# We will create individual router files (e.g., auth.py, chat.py) later.

from fastapi import APIRouter
from .auth import auth_router
from .health import health_router
from .chat import chat_router # Import chat router
from .crm import crm_router   # Import CRM router
from .logs import logs_router  # Import logs router

api_router = APIRouter()

# Include API routes
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"]) # Add chat router
api_router.include_router(crm_router, prefix="/crm", tags=["CRM"])     # Add CRM router
api_router.include_router(logs_router, prefix="/logs", tags=["Logs"])  # Add logs router

# This file serves as the main entry point for API version 1.
