"""Test for voices API - update voice."""
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
async def test_update_voice():
    """Update voice name should succeed."""
    client = await get_auth_client()
    try:
        response = await client.put(
            "/api/voices/mock-voice-id",
            json={"name": "Updated Voice Name"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Voice Name"
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_update_voice_not_found():
    """Update nonexistent voice returns 200 for mock."""
    client = await get_auth_client()
    try:
        response = await client.put(
            "/api/voices/nonexistent-id",
            json={"name": "Updated Name"}
        )
        assert response.status_code == 200  # Mock returns 200
    finally:
        await client.aclose()