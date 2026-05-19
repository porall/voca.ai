"""Test for AI services (Suno + Reecho)."""
import pytest
from app.services.suno import SunoService
from app.services.reecho import ReechoService


@pytest.mark.asyncio
async def test_suno_generate_music():
    """Suno should generate music from prompt."""
    service = SunoService()
    result = await service.generate_music(
        prompt="Upbeat summer pop song",
        duration=180
    )
    
    assert "audio_url" in result
    assert result["status"] == "completed"
    assert result["duration"] == 180
    await service.close()


@pytest.mark.asyncio
async def test_suno_get_status():
    """Suno should return generation status."""
    service = SunoService()
    result = await service.get_status("test-id-123")
    
    assert result["status"] == "completed"
    await service.close()


@pytest.mark.asyncio
async def test_reecho_clone_voice():
    """Reecho should clone voice."""
    service = ReechoService()
    result = await service.clone_voice(
        audio_url="https://example.com/voice.mp3",
        name="My Voice"
    )
    
    assert "voice_id" in result
    assert result["name"] == "My Voice"
    assert result["status"] == "ready"
    await service.close()


@pytest.mark.asyncio
async def test_reecho_synthesize():
    """Reecho should synthesize speech."""
    service = ReechoService()
    result = await service.synthesize(
        text="Hello world",
        voice_id="voice-123"
    )
    
    assert "audio_url" in result
    assert result["voice_id"] == "voice-123"
    await service.close()


@pytest.mark.asyncio
async def test_reecho_synthesize_singing():
    """Reecho should synthesize singing."""
    service = ReechoService()
    result = await service.synthesize_singing(
        lyrics="La la la",
        music_url="https://example.com/music.mp3",
        voice_id="voice-123"
    )
    
    assert "audio_url" in result
    assert result["status"] == "completed"
    await service.close()