from app.repositories.user_repository import UserRepository
from app.models.user_model import User
from app.schemas.auth_schema import UserCreate, UserLogin, Token
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, user_in: UserCreate) -> dict:
        # Legacy: Manual registration is being replaced by Supabase Auth
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Registration must be performed via Supabase Auth")

    async def login(self, user_in: UserLogin) -> Token:
        # Legacy: Manual login is being replaced by Supabase Auth
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Login must be performed via Supabase Auth")
