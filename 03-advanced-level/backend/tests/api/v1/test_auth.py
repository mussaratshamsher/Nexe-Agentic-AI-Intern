import pytest
import httpx
from app.schemas.user import UserCreate, UserResponse, UserInDB # For type hinting and checking response models
from app.core.security import get_password_hash # Useful for setting up test users if needed

# Mark all tests in this module as asyncio tests
pytestmark = pytest.mark.asyncio

# This test file will require a running app and potentially a test DB session fixture.
# The conftest.py provides `async_client` and `test_db_session`.

async def test_register_user_success(async_client: httpx.AsyncClient, test_db_session):
    """
    Tests successful user registration.
    """
    user_data = UserCreate(email="testuser@example.com", password="password123", role="user")
    response = await async_client.post("/auth/register", json=user_data.model_dump())
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["email"] == "testuser@example.com"
    assert "hashed_password" not in response_data # Ensure password is not returned
    assert "id" in response_data
    assert "created_at" in response_data

async def test_register_user_duplicate_email(async_client: httpx.AsyncClient, test_db_session):
    """
    Tests user registration with an email that already exists.
    """
    # First, register a user successfully
    user_data_initial = UserCreate(email="duplicate@example.com", password="password123", role="user")
    await async_client.post("/auth/register", json=user_data_initial.model_dump())
    
    # Try to register the same user again
    user_data_duplicate = UserCreate(email="duplicate@example.com", password="anotherpassword", role="user")
    response = await async_client.post("/auth/register", json=user_data_duplicate.model_dump())
    
    assert response.status_code == 400 # BadRequestException for duplicate email
    assert response.json()["detail"] == "User with email duplicate@example.com already exists."

async def test_login_success(async_client: httpx.AsyncClient, test_db_session):
    """
    Tests successful user login.
    """
    # Register a user first
    user_data_register = UserCreate(email="login_test@example.com", password="secure_password", role="user")
    await async_client.post("/auth/register", json=user_data_register.model_dump())
    
    # Attempt to log in with correct credentials
    login_data = UserCreate(email="login_test@example.com", password="secure_password") # Reusing UserCreate for login data shape
    response = await async_client.post("/auth/login", json=login_data.model_dump())
    
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"] == "bearer"

async def test_login_invalid_credentials(async_client: httpx.AsyncClient, test_db_session):
    """
    Tests login with incorrect password.
    """
    # Register a user first
    user_data_register = UserCreate(email="invalid_login@example.com", password="correct_password", role="user")
    await async_client.post("/auth/register", json=user_data_register.model_dump())
    
    # Attempt to log in with incorrect password
    login_data_wrong_password = UserCreate(email="invalid_login@example.com", password="wrong_password")
    response = await async_client.post("/auth/login", json=login_data_wrong_password.model_dump())
    
    assert response.status_code == 401 # UnauthorizedException
    assert response.json()["detail"] == "Incorrect email or password."

async def test_login_nonexistent_user(async_client: httpx.AsyncClient):
    """
    Tests login with an email that does not exist.
    """
    login_data_nonexistent = UserCreate(email="nonexistent@example.com", password="any_password")
    response = await async_client.post("/auth/login", json=login_data_nonexistent.model_dump())
    
    assert response.status_code == 401 # UnauthorizedException
    assert response.json()["detail"] == "Incorrect email or password."
