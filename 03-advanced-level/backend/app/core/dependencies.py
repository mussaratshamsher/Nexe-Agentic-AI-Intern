from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.execution_repository import ExecutionRepository
from app.services.auth_service import AuthService
from app.core.security import verify_supabase_token
from app.models.user_model import User

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_customer_repo(db: AsyncSession = Depends(get_db)) -> CustomerRepository:
    return CustomerRepository(db)

def get_ticket_repo(db: AsyncSession = Depends(get_db)) -> TicketRepository:
    return TicketRepository(db)

def get_execution_repo(db: AsyncSession = Depends(get_db)) -> ExecutionRepository:
    return ExecutionRepository(db)

def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)

async def get_current_user(
    token_payload: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    email: str = token_payload.get("email")
    if email is None:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(email)
    
    if user is None:
        # Auto-register user from SSO data
        new_user = User(email=email, hashed_password="sso_user")
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        user = new_user
        
    return user
