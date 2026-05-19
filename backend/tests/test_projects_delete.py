"""Test for project delete functionality."""
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
async def test_delete_project():
    """Deleting a project should remove it from the list."""
    client = await get_auth_client()
    try:
        # Create a project first
        create_resp = await client.post(
            "/api/projects",
            json={"name": "Test Project to Delete"}
        )
        assert create_resp.status_code == 200
        project_id = create_resp.json()["id"]
        
        # Verify it exists
        get_resp = await client.get(f"/api/projects/{project_id}")
        assert get_resp.status_code == 200
        
        # Delete the project
        delete_resp = await client.delete(f"/api/projects/{project_id}")
        assert delete_resp.status_code == 200
        assert delete_resp.json()["status"] == "deleted"
        
        # Verify it's gone
        get_after = await client.get(f"/api/projects/{project_id}")
        assert get_after.status_code == 404
    finally:
        await client.aclose()