import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

# Application Core Components
from app.config.settings import settings
from app.db.session import get_db_session
from app.core.security import get_current_user # Placeholder for auth dependency
from app.logs.logger import setup_logger

# Agents
from app.agents.master_orchestrator import MasterOrchestratorAgent
# Specialized agents (will be imported and initialized below)
# from app.agents.sales_agent import SalesAgent
# from app.agents.support_agent import SupportAgent
# from app.agents.project_manager_agent import ProjectManagerAgent
# from app.agents.content_agent import ContentAgent

# Orchestration
from app.orchestration.orchestrator import OrchestrationManager

# Tools & Services
from app.tools.tool_manager import ToolManager, tool_manager # Use the singleton instance
from app.services.execution_log_service import MockExecutionLogService # Mock for now

# API Routes
from app.api.v1.endpoints import api_router # This aggregates all v1 routers

# Setup application logger
logger = setup_logger(__name__)

# --- Initialize Global Services ---
# These should be initialized once and potentially shared.
# For now, we use mock services for logging and tool management.
execution_log_service = MockExecutionLogService() # Placeholder

# Initialize LLM for agents
# Use a powerful model for the orchestrator, like gpt-4o or gpt-4
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=settings.openai_api_key)

# Initialize OrchestrationManager and register all agents
orchestration_manager = OrchestrationManager(
    tool_manager=tool_manager,
    execution_log_service=execution_log_service
)

# --- Agent Initialization and Registration ---
# Import and instantiate specialized agents, then register them
# This ensures they are available for the Master Orchestrator and ToolManager
try:
    from app.agents.sales_agent import SalesAgent
    from app.agents.support_agent import SupportAgent
    from app.agents.project_manager_agent import ProjectManagerAgent
    from app.agents.content_agent import ContentAgent

    # Instantiate and register agents
    sales_agent = SalesAgent(llm=llm, tool_manager=tool_manager, execution_log_service=execution_log_service)
    orchestration_manager.agents[sales_agent.name] = sales_agent # Add to orchestrator's agent dict
    tool_manager.register_agent(sales_agent) # Register for discovery

    support_agent = SupportAgent(llm=llm, tool_manager=tool_manager, execution_log_service=execution_log_service)
    orchestration_manager.agents[support_agent.name] = support_agent
    tool_manager.register_agent(support_agent)

    pm_agent = ProjectManagerAgent(llm=llm, tool_manager=tool_manager, execution_log_service=execution_log_service)
    orchestration_manager.agents[pm_agent.name] = pm_agent
    tool_manager.register_agent(pm_agent)

    content_agent = ContentAgent(llm=llm, tool_manager=tool_manager, execution_log_service=execution_log_service)
    orchestration_manager.agents[content_agent.name] = content_agent
    tool_manager.register_agent(content_agent)
    
    logger.info(f"Registered specialized agents: {', '.join(agent.name for agent in [sales_agent, support_agent, pm_agent, content_agent])}")

except ImportError as e:
    logger.error(f"Failed to import agent classes: {e}. Ensure agent files are correctly placed and imports are correct.")
except Exception as e:
    logger.error(f"An error occurred during agent initialization: {e}", exc_info=True)


# --- FastAPI App Initialization ---
app = FastAPI(
    title=settings.app_name,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    debug=settings.debug,
)

# --- Middlewares ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Routes ---
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint, redirects to API documentation."""
    return RedirectResponse(url=f"{settings.api_v1_str}/docs")

# Include API v1 routes
app.include_router(api_router, prefix=settings.api_v1_str)

# --- Application Startup/Shutdown Events ---
@app.on_event("startup")
async def startup_event():
    """
    Actions to perform when the application starts.
    - Potentially run database migrations (e.g., Alembic).
    - Initialize any services that require a running application context.
    """
    logger.info("Application startup...")
    # In a real app, you might run database migrations here.
    # For example: await run_migrations()
    # Or ensure DB connection pool is ready.
    logger.info("Application started.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform when the application shuts down.
    - Close database connections.
    - Clean up resources.
    """
    logger.info("Application shutting down...")
    # Close database engine if not managed by sessionmaker auto-closing
    # await engine.dispose() # If engine is accessible here
    logger.info("Application shut down.")

if __name__ == "__main__":
    # This block is for running the app directly with uvicorn for development.
    # For production, uvicorn will be run by a process manager like Gunicorn or directly by Render.
    logger.info("Starting FastAPI server with uvicorn...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug # Reload on file changes in debug mode
    )
