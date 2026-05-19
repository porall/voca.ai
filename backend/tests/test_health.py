"""
Test for health check endpoint.
Following TDD: RED first - should fail initially.
"""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_health_check_returns_ok():
    """Health check should return healthy status."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_health_check_has_correct_content_type():
    """Health check should return JSON."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/health")
    
    assert response.headers["content-type"] == "application/json"