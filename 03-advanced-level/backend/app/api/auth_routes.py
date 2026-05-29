from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# Legacy auth routes have been removed in favor of Supabase Auth.
