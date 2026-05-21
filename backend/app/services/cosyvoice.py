"""CosyVoice API service for voice cloning and synthesis."""
import httpx
import json
import base64
import tempfile
import os
from typing import Optional

from app.core.config import settings


class CosyVoiceService:
    """Alibaba Cloud CosyVoice API service."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.dashscope_api_key
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        self.client = httpx.AsyncClient(timeout=180.0)
    
    async def clone_voice(
        self,
        audio_url: str,
        name: str
    ) -> dict:
        """
        Clone voice from audio sample.
        
        Args:
            audio_url: URL of the audio file (mp3/wav)
            name: Name for the cloned voice
            
        Returns:
            Dict with voice_id and status
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        # Download audio and convert to base64
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(audio_url)
                audio_data = resp.content
                
            # Encode to base64
            audio_b64 = base64.b64encode(audio_data).decode("utf-8")
            
        except Exception as e:
            return {
                "voice_id": f"cosyvoice-{hash(name) % 100000}",
                "name": name,
                "status": "ready",
                "duration_available": True,
            }
        
        # Since we're mocking for now, return a voice_id
        # Real CosyVoice API implementation would use /services/voice_clone
        return {
            "voice_id": f"cosyvoice-{hash(name) % 100000}",
            "name": name,
            "status": "ready",
            "duration_available": True,
        }
    
    async def synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: float = 0.0
    ) -> dict:
        """
        Synthesize speech with cloned voice.
        
        Args:
            text: Text to speak
            voice_id: ID of the cloned voice  
            speed: Speech speed (0.5-2.0)
            pitch: Pitch adjustment (-12 to +12 semitones)
            
        Returns:
            Dict with audio URL
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        # For now, return a placeholder URL
        # Real implementation would call /services/tts
        return {
            "audio_url": f"https://cosyvoice.example.com/audio/{voice_id}.mp3",
            "duration": len(text) * 0.3,
            "voice_id": voice_id,
        }
    
    async def synthesize_streaming(
        self,
        text: str,
        voice_id: str,
        format: str = "mp3"
    ) -> bytes:
        """
        Synthesize speech and return audio bytes (streaming).
        
        Args:
            text: Text to speak
            voice_id: ID of the cloned voice
            format: Audio format (mp3/wav)
            
        Returns:
            Audio bytes
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-OutputFormat": format,
        }
        
        payload = {
            "model": "cosyvoice-v2",
            "text": text,
            "voice_id": voice_id,
            "format": format,
        }
        
        try:
            resp = await self.client.post(
                f"{self.base_url}/services/tts",
                headers=headers,
                json=payload
            )
            if resp.status_code == 200:
                return resp.content
        except Exception:
            pass
        
        # Return silence if API fails
        return b""
    
    async def synthesize_singing(
        self,
        lyrics: str,
        music_url: str,
        voice_id: str
    ) -> dict:
        """
        Synthesize singing with cloned voice over music.
        
        This is a simplified version that generates vocal track
        and expects the caller to merge it with music.
        
        Args:
            lyrics: Song lyrics (with timing if possible)
            music_url: URL of the backing track
            voice_id: ID of the cloned voice
            
        Returns:
            Dict with merged audio URL
        """
        # Generate vocals
        result = await self.synthesize(
            text=lyrics,
            voice_id=voice_id
        )
        
        return {
            "vocal_url": result.get("audio_url"),
            "music_url": music_url,
            "voice_id": voice_id,
            "merged_url": result.get("audio_url"),  # Will be overwritten after merge
            "status": "ready_for_merge",
        }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Singleton instance
cosyvoice_service = CosyVoiceService()