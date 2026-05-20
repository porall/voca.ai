"""Voice API routes for voice cloning."""
import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.db import get_db, User, Voice
from app.api.auth import get_current_user, UserResponse
from app.services.reecho import reecho_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Storage directory for uploaded audio files
VOICE_STORAGE_DIR = "/home/ubuntu/voca.ai/backend/voices"


# Models
class VoiceResponse(BaseModel):
    """Voice response model."""
    id: str
    name: str
    audio_url: Optional[str]
    duration_secs: Optional[float]
    is_default: bool
    status: str
    created_at: str

    class Config:
        from_attributes = True


def voice_to_response(voice: Voice) -> VoiceResponse:
    """Convert Voice model to response."""
    return VoiceResponse(
        id=voice.id,
        name=voice.name,
        audio_url=voice.audio_url,
        duration_secs=voice.duration_secs,
        is_default=voice.is_default,
        status=voice.status,
        created_at=voice.created_at.isoformat() if voice.created_at else "",
    )


# Routes
@router.get("", response_model=List[VoiceResponse])
async def list_voices(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all voices for current user."""
    voices = db.query(Voice).filter(Voice.user_id == current_user.id).all()
    return [voice_to_response(v) for v in voices]


@router.post("/upload", response_model=VoiceResponse, status_code=status.HTTP_201_CREATED)
async def upload_voice(
    name: str = Form(...),
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload audio file to clone voice."""
    # Validate file type
    if not file.filename.endswith((".mp3", ".wav", ".m4a", ".flac")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Use MP3, WAV, M4A, or FLAC.",
        )
    
    # Create storage directory
    os.makedirs(VOICE_STORAGE_DIR, exist_ok=True)
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    voice_id = str(uuid.uuid4())
    filename = f"{voice_id}{file_ext}"
    file_path = os.path.join(VOICE_STORAGE_DIR, filename)
    
    # Save uploaded file
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 10MB.",
        )
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Create local URL for the file
    audio_url = f"/voices/{filename}"
    
    # Call Reecho API to clone voice (in background)
    # For now, mark as ready (mock)
    try:
        result = await reecho_service.clone_voice(
            audio_url=f"file://{file_path}",
            name=name,
        )
        voice_status = result.get("status", "ready")
    except Exception as e:
        # If Reecho fails, still save locally with error status
        voice_status = "failed"
    
    # Save to database
    db_voice = Voice(
        id=voice_id,
        user_id=current_user.id,
        name=name,
        audio_url=audio_url,
        duration_secs=content.size / 44100 if hasattr(content, 'size') else 10.0,  # Estimate
        is_default=False,
        status=voice_status,
    )
    db.add(db_voice)
    db.commit()
    db.refresh(db_voice)
    
    return voice_to_response(db_voice)


@router.delete("/{voice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voice(
    voice_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a voice."""
    voice = db.query(Voice).filter(
        Voice.id == voice_id,
        Voice.user_id == current_user.id,
    ).first()
    
    if not voice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voice not found",
        )
    
    # Delete local file if exists
    if voice.audio_url:
        file_path = os.path.join(VOICE_STORAGE_DIR, os.path.basename(voice.audio_url))
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.delete(voice)
    db.commit()
    
    return None