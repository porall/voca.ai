"""Test for AI services (Suno + Reecho)."""
import pytest
from app.services.suno import SunoService
from app.services.reecho import ReechoService


@pytest.mark.asyncio
async def test_suno_get_status():
    """Suno status check is free (read-only)."""
    service = SunoService()
    result = await service.get_task_status(104191882)
    assert "status" in result
    await service.close()


# Skip - costs credits
# @pytest.mark.asyncio
# async def test_suno_generate_music():
#     result = await service.generate_music(prompt="Test", duration=180)


@pytest.mark.asyncio
async def test_reecho_clone_voice():
    """Reecho voice cloning - will make real API call if enabled."""
    pass  # Skipped to avoid real API calls


@pytest.mark.asyncio
async def test_reecho_synthesize():
    """Reecho synthesis - will make real API call if enabled."""
    pass  # Skipped to avoid real API calls