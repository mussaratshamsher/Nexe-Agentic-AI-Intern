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
auth_router = APIRouter()

# Dependency to get current user from token (placeholder for now)
# async def get_current_user(token: str = Depends(oauth2_scheme)): # Assuming oauth2_scheme is defined later
#     payload = verify_jwt_token(token)
#     if payload is None:
#         raise UnauthorizedException()
#     user_id = payload.get("sub")
#     if user_id is None:
#         raise UnauthorizedException()
#     # In a real app, fetch user from DB using user_id
#     # user = await user_repository.get(user_id)
#     # if user is None:
#     #     raise UnauthorizedException("User not found")
#     # return user
#     return {"user_id": user_id, "role": "user"} # Dummy user for now

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Register a new user.
    """
    logger.info(f"Attempting to register user with email: {user_data.email}")
    
    # Check if user already exists
    # Assuming user_repository is available and handles DB operations
    # This is a simplified example using direct ORM access for now
    
    # Existing user check will be implemented when User repository is ready.
    # For now, we'll directly try to create and catch IntegrityError.

    try:
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role # Role can be specified or defaults to 'user'
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"User registered successfully: {new_user.email}")
        # Return user details, excluding password
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            role=new_user.role,
            created_at=new_user.created_at
        )

    except IntegrityError:
        await db.rollback()
        logger.warning(f"Registration failed: Email {user_data.email} already exists.")
        raise BadRequestException(detail=f"User with email {user_data.email} already exists.")
    except Exception as e:
        await db.rollback()
        logger.error(f"Registration failed for {user_data.email}: {e}", exc_info=True)
        raise InternalServerErrorException(detail="An error occurred during registration.")

@auth_router.post("/login")
async def login_for_access_token(
    form_data: UserCreate, # Reusing UserCreate for simplicity, but normally a dedicated LoginSchema
    db: AsyncSession = Depends(get_db_session)
):
    """
    Login user and return access and refresh tokens.
    """
    logger.info(f"Attempting to log in user with email: {form_data.email}")

    # Fetch user from DB (this part would typically use a repository)
    # In a real app, you would fetch the user by email from the database.
    # For this example, we'll simulate fetching and verifying.
    
    # Placeholder: In a real app, use a UserRepostory
    # user = await user_repository.get_by_email(form_data.email)
    
    # Simulate fetching user data (replace with actual DB query)
    # For testing, we'll assume a user exists or will be created.
    # If the user is not found, return unauthorized.
    
    # Fetch user by email using SQLAlchemy 2.0 style select
    try:
        stmt = select(User).where(User.email == form_data.email)
        user_orm = await db.execute(stmt)
        user = user_orm.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Database error during login for {form_data.email}: {e}", exc_info=True)
        raise InternalServerErrorException(detail="Database error during login.")


    if user is None or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed for email: {form_data.email}. Invalid credentials.")
        raise UnauthorizedException(detail="Incorrect email or password.")

    logger.info(f"User logged in successfully: {user.email}")

    # Create tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Add /auth/refresh_token endpoint later

# --- Helper to aggregate routers ---
# In endpoints.py, we will import and include these routers.
# For now, these are standalone.
