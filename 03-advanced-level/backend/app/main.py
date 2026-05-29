from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback
from app.api import (
    auth_routes, 
    chat_routes, 
    customer_routes, 
    ticket_routes, 
    log_routes,
    health_routes,
    knowledge_routes,
    webhook_routes,
    contact_routes
)
from app.services.ingestion_service import IngestionService

app = FastAPI(title="AI Business Operations Manager API")

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.on_event("startup")
async def startup_event():
    IngestionService.start_background_tasks()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# Include routers with API versioning prefix
app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(chat_routes.router, prefix="/api/v1")
app.include_router(customer_routes.router, prefix="/api/v1")
app.include_router(ticket_routes.router, prefix="/api/v1")
app.include_router(log_routes.router, prefix="/api/v1")
app.include_router(health_routes.router, prefix="/api/v1")
app.include_router(knowledge_routes.router, prefix="/api/v1")
app.include_router(webhook_routes.router, prefix="/api/v1")
app.include_router(contact_routes.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
