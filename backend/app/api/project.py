"""Project/Song API endpoints."""
from datetime import datetime
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, model_serializer

from app.models.db import Project, get_db
from app.services.project import project_service
from app.api.auth import get_current_user, UserResponse

router = APIRouter(prefix="", tags=["projects"])


# Schemas
class ProjectCreate(BaseModel):
    name: str
    gpt_description: Optional[str] = None
    lyrics: Optional[str] = None
    music_genre: Optional[str] = None
    style: Optional[str] = None
    voice_id: Optional[str] = None
    mv: str = "chirp-fenix"
    make_instrumental: bool = False


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    gpt_description: Optional[str] = None
    lyrics: Optional[str] = None
    music_genre: Optional[str] = None
    style: Optional[str] = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str
    gpt_description: Optional[str] = None
    lyrics: Optional[str] = None
    music_genre: Optional[str] = None
    style: Optional[str] = None
    voice_id: Optional[str] = None
    task_id: Optional[str] = None
    suno_title: Optional[str] = None
    suno_id: Optional[str] = None
    mv: str = "chirp-fenix"
    duration: Optional[int] = None
    music_url: Optional[str] = None
    cover_url: Optional[str] = None
    vocal_url: Optional[str] = None
    final_url: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    points_cost: int = 0
    created_at: Union[str, datetime]
    
    @model_serializer(mode='wrap')
    def serialize(self, handler):
        data = handler(self)
        if isinstance(data.get('created_at'), datetime):
            data['created_at'] = data['created_at'].isoformat()
        return data


class GenerateResponse(BaseModel):
    task_ids: List[int]
    message: str


class StatusResponse(BaseModel):
    task_id: str
    status: str
    audio_url: Optional[str] = None
    cover_url: Optional[str] = None
    duration: Optional[int] = None
    title: Optional[str] = None
    lyrics: Optional[str] = None
    error_msg: Optional[str] = None
    points_cost: int = 0


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new song project."""
    project = project_service.create(
        db=db,
        user_id=current_user.id,
        name=data.name,
        gpt_description=data.gpt_description,
        lyrics=data.lyrics,
        music_genre=data.music_genre,
        style=data.style,
        voice_id=data.voice_id,
        mv=data.mv,
        make_instrumental=data.make_instrumental,
    )
    return project


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List user's projects."""
    projects = project_service.list_by_user(
        db=db, 
        user_id=current_user.id, 
        limit=limit, 
        offset=offset
    )
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a project by ID."""
    project = project_service.get(db=db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a project."""
    project = project_service.get(db=db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_service.delete(db=db, project_id=project_id)
    return None


@router.post("/{project_id}/generate", response_model=GenerateResponse)
async def generate_song(
    project_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Generate music for a project."""
    project = project_service.get(db=db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.status == "processing":
        raise HTTPException(status_code=400, detail="Already generating")
    
    try:
        result = await project_service.generate(project_id=project_id, db=db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}/status", response_model=StatusResponse)
async def check_status(
    project_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Check song generation status."""
    project = project_service.get(db=db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        result = await project_service.check_status(project_id=project_id, db=db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))