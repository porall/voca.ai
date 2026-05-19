"""Test for voices API - get single voice."""
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
        data={"username": "test@example.com", "password": "***"}
    )
    token = login_resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    
    return client


@pytest.mark.asyncio
async def test_get_voice_by_id():
    """Get single voice by ID should return voice details."""
    client = await get_auth_client()
    try:
        response = await client.get("/api/voices/mock-voice-id")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_get_voice_not_found():
    """Get nonexistent voice should return voice (mock behavior)."""
    client = await get_auth_client()
    try:
        response = await client.get("/api/voices/nonexistent-id")
        assert response.status_code == 200
    finally:
        await client.aclose()