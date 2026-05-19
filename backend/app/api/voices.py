"""Voice management API routes."""
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.api.auth import get_current_user, UserResponse

router = APIRouter()


# Models
class VoiceResponse(BaseModel):
    """Voice clone response."""
    id: str
    name: str
    audio_url: str
    duration_secs: float
    is_default: bool
    status: str
    created_at: datetime


class VoiceCreate(BaseModel):
    """Voice creation request."""
    name: str


# Routes
@router.get("", response_model=List[VoiceResponse])
async def get_voices(current_user: UserResponse = Depends(get_current_user)):
    """Get user's voice clones."""
    # TODO: Get from DB
    return []


@router.post("", response_model=VoiceResponse)
async def create_voice(
    name: str,
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
):
    """Upload audio to create a voice clone."""
    # TODO: Upload to S3, call Reecho API to clone
    return VoiceResponse(
        id="mock-voice-id",
        name=name,
        audio_url="https://example.com/voice.mp3",
        duration_secs=10.0,
        is_default=False,
        status="ready",
        created_at=datetime.utcnow(),
    )


@router.delete("/{voice_id}")
async def delete_voice(
    voice_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """Delete a voice clone."""
    # TODO: Delete from DB and S3
    return {"status": "deleted"}