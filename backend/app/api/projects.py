"""Project management API routes."""
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.auth import get_current_user, UserResponse

router = APIRouter()


# Models
class ProjectResponse(BaseModel):
    """Project response."""
    id: str
    name: str
    lyrics: Optional[str]
    music_genre: Optional[str]
    style: Optional[str]
    voice_id: Optional[str]
    music_url: Optional[str]
    vocal_url: Optional[str]
    final_url: Optional[str]
    status: str
    created_at: datetime


class ProjectCreate(BaseModel):
    """Project creation request."""
    name: str
    lyrics: Optional[str] = None
    music_genre: Optional[str] = None
    style: Optional[str] = None
    voice_id: Optional[str] = None


class GenerateRequest(BaseModel):
    """AI generation request."""
    prompt: str
    duration: Optional[int] = 180  # seconds


# Routes
@router.get("", response_model=List[ProjectResponse])
async def get_projects(current_user: UserResponse = Depends(get_current_user)):
    """Get user's projects."""
    # TODO: Get from DB
    return []


@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    """Create a new project."""
    # TODO: Save to DB
    return ProjectResponse(
        id="mock-project-id",
        name=project.name,
        lyrics=project.lyrics,
        music_genre=project.music_genre,
        style=project.style,
        voice_id=project.voice_id,
        music_url=None,
        vocal_url=None,
        final_url=None,
        status="draft",
        created_at=datetime.utcnow(),
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get project details."""
    # TODO: Get from DB
    return ProjectResponse(
        id=project_id,
        name="Mock Project",
        lyrics=None,
        music_genre=None,
        style=None,
        voice_id=None,
        music_url=None,
        vocal_url=None,
        final_url=None,
        status="draft",
        created_at=datetime.utcnow(),
    )


@router.post("/{project_id}/generate")
async def generate_song(
    project_id: str,
    request: GenerateRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """Trigger AI song generation."""
    # TODO: Call Suno + Reecho APIs
    return {
        "status": "processing",
        "message": "Generation started",
        "project_id": project_id,
    }


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """Delete a project."""
    # TODO: Delete from DB
    return {"status": "deleted"}