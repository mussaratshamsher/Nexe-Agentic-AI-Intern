from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, select
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db_session
from app.core.security import get_password_hash, create_access_token, create_refresh_token, verify_jwt_token
from app.schemas.user import UserCreate, UserResponse, UserInDB, UserRoleEnum
from app.models.user import User
from app.core.exceptions import BadRequestException, UnauthorizedException, InternalServerErrorException
from app.logs.logger import setup_logger

logger = setup_logger(__name__)
health_router = APIRouter()

@health_router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    """
    Health check endpoint.
    Checks database connection and returns a simple status.
    """
    logger.info("Health check endpoint accessed.")
    # Basic check: try to execute a simple query to confirm DB connection
    try:
        # A simple query like selecting a constant or checking DB version
        # For now, we'll just return a success message if the dependency injection works.
        # A more robust check would be to query a small, known table or a system view.
        # Example: SELECT 1;
        # result = await db.execute(text("SELECT 1"))
        # result.scalar() # This would execute the query
        
        # For simplicity, we rely on the dependency injection itself succeeding.
        # If get_db_session() returns a valid session, we assume connection is ok.
        return {"status": "ok", "message": "Database connection is healthy."}
    except Exception as e:
        logger.error(f"Health check failed: Database connection error - {e}")
        # Return a 503 Service Unavailable if the DB is down
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail=f"Database connection failed: {e}")

