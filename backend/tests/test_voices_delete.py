"""Test for voices API - delete voice."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_delete_voice():
    """Deleting a voice should remove it from the list."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # Get token first
        login_resp = await client.post(
            "/api/auth/login",
            data={"username": "test@example.com", "password": "password123"}
        )
        token = login_resp.json()["access_token"]
        
        # Create a voice first - using multipart form data (name is query param)
        voice_resp = await client.post(
            "/api/voices?name=Test Voice",
            files={"file": ("test.mp3", b"fake audio data", "audio/mpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
        voice_id = voice_resp.json()["id"]
        
        # Delete the voice
        del_resp = await client.delete(
            f"/api/voices/{voice_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert del_resp.status_code == 200
        assert del_resp.json()["status"] == "deleted"