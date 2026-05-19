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


class VoiceUpdate(BaseModel):
    """Voice update request."""
    name: str | None = None
    is_default: bool | None = None


@router.put("/{voice_id}", response_model=VoiceResponse)
async def update_voice(
    voice_id: str,
    voice_update: VoiceUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    """Update a voice clone."""
    # TODO: Update in DB
    return VoiceResponse(
        id=voice_id,
        name=voice_update.name or "Updated Voice",
        audio_url="https://example.com/voice.mp3",
        duration_secs=10.0,
        is_default=voice_update.is_default or False,
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


@router.get("/{voice_id}", response_model=VoiceResponse)
async def get_voice(
    voice_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get a voice clone by ID."""
    # TODO: Get from DB
    return VoiceResponse(
        id=voice_id,
        name="Mock Voice",
        audio_url="https://example.com/voice.mp3",
        duration_secs=10.0,
        is_default=False,
        status="ready",
        created_at=datetime.utcnow(),
    )