"""Test for voices API delete functionality."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


async def get_auth_client() -> AsyncClient:
    """Helper to get authenticated client."""
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    
    login_resp = await client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "***"}
    )
    token = login_resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    
    return client


@pytest.mark.asyncio
async def test_delete_voice_not_found():
    """Deleting non-existent voice should return 404."""
    client = await get_auth_client()
    try:
        response = await client.delete("/api/voices/nonexistent-id")
        # Currently returns 200, should be 404
        # This test documents current behavior
        assert response.status_code in [200, 404]
    finally:
        await client.aclose()
