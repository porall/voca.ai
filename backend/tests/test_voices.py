"""Test for voices API - voice cloning management."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


async def get_auth_client() -> AsyncClient:
    """Helper to get authenticated client."""
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    
    # Login first
    login_resp = await client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    
    return client


@pytest.mark.asyncio
async def test_get_voices_requires_auth():
    """Get voices should require authentication."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/voices")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_voices_empty_list():
    """Get voices should return empty list for new user."""
    client = await get_auth_client()
    try:
        response = await client.get("/api/voices")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_get_voices_with_wrong_token():
    """Get voices should fail with wrong token."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        client.headers["Authorization"] = "Bearer wrong-token"
        response = await client.get("/api/voices")
    
    assert response.status_code == 401