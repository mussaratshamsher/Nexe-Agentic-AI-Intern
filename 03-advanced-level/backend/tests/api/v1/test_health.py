import pytest
import httpx
from app.config.settings import settings

# Mark all tests in this module as asyncio tests
pytestmark = pytest.mark.asyncio

async def test_health_check(async_client: httpx.AsyncClient):
    """
    Tests the /health endpoint to ensure it returns a 200 OK status and correct message.
    """
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Database connection is healthy."}
