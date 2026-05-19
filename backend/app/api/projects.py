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


class ProjectUpdate(BaseModel):
    """Project update request."""
    name: Optional[str] = None
    lyrics: Optional[str] = None
    music_genre: Optional[str] = None
    style: Optional[str] = None
    voice_id: Optional[str] = None


# In-memory storage for mock data
PROJECTS_DB = {}


# Routes
@router.get("", response_model=List[ProjectResponse])
async def get_projects(current_user: UserResponse = Depends(get_current_user)):
    """Get user's projects."""
    # Return from mock DB
    user_projects = [p for p in PROJECTS_DB.values() if p["user_id"] == current_user.id]
    return user_projects


@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    """Create a new project."""
    project_id = f"proj-{len(PROJECTS_DB) + 1}"
    new_project = ProjectResponse(
        id=project_id,
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
    PROJECTS_DB[project_id] = {**new_project.model_dump(), "user_id": current_user.id}
    return new_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get project details."""
    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Project not found")
    return PROJECTS_DB[project_id]


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    """Update a project."""
    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Project not found")
    
    existing = PROJECTS_DB[project_id]
    if project.name is not None:
        existing["name"] = project.name
    if project.lyrics is not None:
        existing["lyrics"] = project.lyrics
    if project.music_genre is not None:
        existing["music_genre"] = project.music_genre
    if project.style is not None:
        existing["style"] = project.style
    if project.voice_id is not None:
        existing["voice_id"] = project.voice_id
    
    return existing


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
    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Verify ownership
    project = PROJECTS_DB[project_id]
    if project["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    
    del PROJECTS_DB[project_id]
    return {"status": "deleted", "project_id": project_id}