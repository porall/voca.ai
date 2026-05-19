"""Test for projects API - update project functionality."""
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
async def test_update_project():
    """Updating a project should work."""
    client = await get_auth_client()
    try:
        # Create project first
        create_resp = await client.post(
            "/api/projects",
            json={"name": "Original Name", "lyrics": ""}
        )
        assert create_resp.status_code == 200
        project_id = create_resp.json()["id"]

        # Update project
        update_resp = await client.put(
            f"/api/projects/{project_id}",
            json={"name": "Updated Name", "lyrics": "New lyrics"}
        )
        assert update_resp.status_code == 200
        data = update_resp.json()
        assert data["name"] == "Updated Name"
        assert data["lyrics"] == "New lyrics"
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_update_nonexistent_project():
    """Updating nonexistent project should fail."""
    client = await get_auth_client()
    try:
        update_resp = await client.put(
            "/api/projects/nonexistent-id",
            json={"name": "New Name"}
        )
        assert update_resp.status_code == 404
    finally:
        await client.aclose()