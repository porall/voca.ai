"""Suno API service for AI music generation."""
import httpx
import json
from typing import Optional, List
from app.core.config import settings


class SunoService:
    """Suno AI music generation service (open.suno.cn API)."""
    
    BASE_URL = "https://open.suno.cn/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.suno_api_key
        self.client = httpx.AsyncClient(timeout=180.0)
    
    def _get_headers(self) -> dict:
        """Build request headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def get_balance(self) -> dict:
        """
        Get account points balance.
        
        Returns:
            Dict with remaining_points
        """
        response = await self.client.get(
            f"{self.BASE_URL}/points/balance",
            headers=self._get_headers()
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "remaining_points": data.get("data", {}).get("remaining_points", 0)
        }
    
    async def generate_music(
        self,
        gpt_description: Optional[str] = None,
        prompt: Optional[str] = None,
        tags: Optional[str] = None,
        title: Optional[str] = None,
        make_instrumental: bool = False,
        mv: str = "chirp-fenix"
    ) -> dict:
        """
        Generate music using Suno API.
        
        Args:
            gpt_description: AI description prompt (inspiration mode)
            prompt: Custom lyrics (custom_mode=true)
            tags: Music style tags (e.g., "pop, acoustic")
            title: Song title
            make_instrumental: True for instrumental only
            mv: Model version (chirp-fenix, chirp-v4, etc.)
        
        Returns:
            Dict with task_ids
        """
        payload = {
            "make_instrumental": make_instrumental,
            "mv": mv,
        }
        
        if gpt_description:
            payload["gpt_description_prompt"] = gpt_description
        elif prompt:
            payload["prompt"] = prompt
        
        if title:
            payload["title"] = title
        if tags:
            payload["tags"] = tags
        
        response = await self.client.post(
            f"{self.BASE_URL}/music/generate",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "task_ids": data.get("data", {}).get("task_ids", []),
            "message": data.get("message"),
        }
    
    async def get_task_status(self, task_id: int) -> dict:
        """
        Check generation task status.
        
        Args:
            task_id: The numeric task ID (not custom_id)
        
        Returns:
            Dict with status, custom_id, audio_url, etc.
        """
        response = await self.client.get(
            f"{self.BASE_URL}/music/task",
            headers=self._get_headers(),
            params={"id": task_id}
        )
        response.raise_for_status()
        data = response.json()
        
        task_data = data.get("data", {})
        result = task_data.get("result") or {}
        file_info = result.get("fileInfo") or {}
        
        return {
            "task_id": task_data.get("task_id") or task_id,
            "status": task_data.get("status"),  # pending/processing/completed/failed
            "custom_id": result.get("custom_id"),
            "audio_url": file_info.get("mp3Url"),
            "video_url": file_info.get("videoUrl"),
            "cover_url": file_info.get("cosUrl"),
            "duration": file_info.get("duration"),
            "title": result.get("title"),
            "lyrics": result.get("lyrics"),
            "error_msg": task_data.get("error"),
            "points_cost": task_data.get("points_cost"),
            "points_refunded": task_data.get("points_refunded"),
        }
    
    async def get_tasks_status(self, task_ids: List[int], page: int = 1, size: int = 20) -> dict:
        """
        Batch check task status.
        
        Args:
            task_ids: List of task IDs
            page: Page number
            size: Page size
        
        Returns:
            Dict with tasks list
        """
        response = await self.client.get(
            f"{self.BASE_URL}/music/tasks",
            headers=self._get_headers(),
            params={
                "ids": ",".join(map(str, task_ids)),
                "page": page,
                "size": size
            }
        )
        response.raise_for_status()
        data = response.json()
        
        return data.get("data", {})
    
    async def extend_song(
        self,
        custom_id: str,
        title: Optional[str] = None,
        mv: str = "chirp-fenix"
    ) -> dict:
        """
        Extend an existing song.
        
        Args:
            custom_id: The Suno music ID (UUID)
            title: Title for extended part
            mv: Model version
        
        Returns:
            Dict with task_ids
        """
        payload = {
            "task": "extend",
            "continue_clip_id": custom_id,
            "mv": mv,
        }
        
        if title:
            payload["title"] = title
        
        response = await self.client.post(
            f"{self.BASE_URL}/music/generate",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "task_ids": data.get("data", {}).get("task_ids", []),
            "message": data.get("message"),
        }
    
    async def cover_song(
        self,
        custom_id: str,
        tags: str,
        title: Optional[str] = None,
        mv: str = "chirp-fenix"
    ) -> dict:
        """
        Create a cover version.
        
        Args:
            custom_id: The Suno music ID (UUID)
            tags: New style tags
            title: Title for cover
            mv: Model version
        
        Returns:
            Dict with task_ids
        """
        payload = {
            "task": "cover",
            "cover_clip_id": custom_id,
            "tags": tags,
            "mv": mv,
        }
        
        if title:
            payload["title"] = title
        
        response = await self.client.post(
            f"{self.BASE_URL}/music/generate",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "task_ids": data.get("data", {}).get("task_ids", []),
            "message": data.get("message"),
        }
    
    async def upload_reference(self, audio_url: str) -> dict:
        """
        Upload reference audio.
        
        Args:
            audio_url: Public URL to audio file
        
        Returns:
            Dict with task_id
        """
        payload = {"audio_url": audio_url}
        
        response = await self.client.post(
            f"{self.BASE_URL}/music/upload",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "task_id": data.get("data", {}).get("task_id"),
            "message": data.get("message"),
        }
    
    async def convert_wav(
        self,
        task_id: int,
        custom_id: str
    ) -> dict:
        """
        Convert to WAV format.
        
        Args:
            task_id: Numeric task ID
            custom_id: Suno music ID (UUID)
        
        Returns:
            Dict with task_ids
        """
        payload = {
            "task_id": task_id,
            "suno_id": custom_id,
        }
        
        response = await self.client.post(
            f"{self.BASE_URL}/music/convert-wav",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "task_ids": data.get("data", {}).get("task_ids", []),
            "message": data.get("message"),
        }
    
    async def crop_music(
        self,
        custom_id: str,
        start_time: int,
        end_time: int
    ) -> dict:
        """
        Crop music.
        
        Args:
            custom_id: Suno music ID (UUID)
            start_time: Start time in seconds
            end_time: End time in seconds
        
        Returns:
            Dict with task_ids
        """
        payload = {
            "clip_id": custom_id,
            "start_time": start_time,
            "end_time": end_time,
        }
        
        response = await self.client.post(
            f"{self.BASE_URL}/music/crop",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "task_ids": data.get("data", {}).get("task_ids", []),
            "message": data.get("message"),
        }
    
    async def adjust_speed(
        self,
        custom_id: str,
        speed: float
    ) -> dict:
        """
        Adjust music speed.
        
        Args:
            custom_id: Suno music ID (UUID)
            speed: Speed multiplier (0.5 = slow, 2.0 = fast)
        
        Returns:
            Dict with task_ids
        """
        payload = {
            "clip_id": custom_id,
            "speed": speed,
        }
        
        response = await self.client.post(
            f"{self.BASE_URL}/music/speed",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "task_ids": data.get("data", {}).get("task_ids", []),
            "message": data.get("message"),
        }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Singleton instance
suno_service = SunoService()