from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config.settings import settings
from app.logs.logger import setup_logger

logger = setup_logger(__name__)

# Password Hashing
# Using bcrypt as it's recommended for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hashed password."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Handle cases where the hashed_password might be malformed
        logger.error("Invalid hashed password format provided for verification.")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during password verification: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Hashes a plain text password."""
    return pwd_context.hash(password)

# JWT Token Generation and Verification
def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)} # 'sub' for subject (e.g., user ID)
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create JWT token: {e}")
        raise RuntimeError("Could not create JWT token") from e

def create_refresh_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT refresh token."""
    if expires_delta is None:
        # Refresh tokens typically have a longer expiration
        expires_delta = timedelta(days=settings.refresh_token_expire_days)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"} # Add type to distinguish
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create JWT refresh token: {e}")
        raise RuntimeError("Could not create JWT refresh token") from e

def verify_jwt_token(token: str) -> dict | None:
    """Verifies a JWT token and returns the decoded payload."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        # You can add more validation here, e.g., checking token type
        # if payload.get("type") == "refresh": return None
        return payload
    except JWTError as e:
        logger.warning(f"Invalid JWT token: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during JWT verification: {e}")
        return None

# Placeholder for dependency injection for current user
async def get_current_user(token: str):
    # This function would typically be used in API endpoints to get the authenticated user.
    # It would decode the token, find the user in the database, and return the user object.
    # For now, it's a placeholder.
    # Example:
    # payload = verify_jwt_token(token)
    # if payload is None:
    #     raise UnauthorizedException()
    # user_id = payload.get("sub")
    # if user_id is None:
    #     raise UnauthorizedException()
    # user = await user_repository.get(user_id) # Assuming user_repository exists
    # if user is None:
    #     raise UnauthorizedException("User not found")
    # return user
    pass
