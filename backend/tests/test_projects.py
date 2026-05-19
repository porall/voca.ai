"""Test for projects API - song creation projects."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


async def get_auth_client() -> AsyncClient:
    """Helper to get authenticated client."""
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    login_resp = await client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.mark.asyncio
async def test_get_projects_requires_auth():
    """Get projects should require authentication."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/projects")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_projects_empty():
    """Get projects should return empty list."""
    client = await get_auth_client()
    try:
        response = await client.get("/api/projects")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_create_project():
    """Creating a new project should work."""
    client = await get_auth_client()
    try:
        response = await client.post(
            "/api/projects",
            json={
                "name": "My First Song",
                "lyrics": "Hello world\nThis is my song",
                "music_genre": "pop",
                "style": "upbeat"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "My First Song"
        assert "id" in data
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_generate_song_requires_all_params():
    """Generate song should require prompt."""
    client = await get_auth_client()
    try:
        # Create project first
        create_resp = await client.post(
            "/api/projects",
            json={"name": "Test Song"}
        )
        project_id = create_resp.json()["id"]
        
        # Try to generate without prompt
        gen_resp = await client.post(
            f"/api/projects/{project_id}/generate",
            json={}
        )
        assert gen_resp.status_code == 422
    finally:
        await client.aclose()