"""Test for auth API - login and registration."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_login_returns_token():
    """Login should return access token."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/auth/login",
            data={"username": "test@example.com", "password": "password123"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


@pytest.mark.asyncio
async def test_register_creates_user():
    """Registration should create new user."""
    import random
    random_email = f"newuser{random.randint(1000,9999)}@example.com"
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/auth/register",
            json={
                "email": random_email,
                "password": "password123",
                "nickname": "New User"
            }
        )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data


@pytest.mark.asyncio  
async def test_get_me_requires_auth():
    """Get /me endpoint should require authentication."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/auth/me")
    
    assert response.status_code == 401