"""Test for password validation in auth API."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_register_rejects_short_password():
    """Registration should reject passwords shorter than 8 characters."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "short",  # Only 5 chars
                "nickname": "Test User"
            }
        )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_rejects_missing_password():
    """Registration should reject missing password."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                # No password field
                "nickname": "Test User"
            }
        )
    
    assert response.status_code == 422  # Validation error