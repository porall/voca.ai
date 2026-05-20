"""Project/Song service for managing songs."""
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.models.db import Project
from app.services.suno import suno_service


class ProjectService:
    """Service for managing song projects."""
    
    @staticmethod
    def create(
        db: Session,
        user_id: str,
        name: str,
        gpt_description: Optional[str] = None,
        lyrics: Optional[str] = None,
        music_genre: Optional[str] = None,
        style: Optional[str] = None,
        voice_id: Optional[str] = None,
        mv: str = "chirp-fenix",
        make_instrumental: bool = False,
    ) -> Project:
        """Create a new song project."""
        project = Project(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            gpt_description=gpt_description,
            lyrics=lyrics,
            music_genre=music_genre,
            style=style,
            voice_id=voice_id,
            mv=mv,
            status="pending",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    @staticmethod
    async def generate(project_id: str, db: Session) -> dict:
        """Generate music for a project via Suno API."""
        # Get project
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        # Update status
        project.status = "processing"
        db.commit()
        
        # Call Suno API
        result = await suno_service.generate_music(
            gpt_description=project.gpt_description,
            prompt=project.lyrics,
            tags=project.music_genre,
            title=project.name,
            make_instrumental=bool(project.voice_id),  # If voice selected, generate instrumental
            mv=project.mv,
        )
        
        task_ids = result.get("task_ids", [])
        if task_ids:
            project.task_id = str(task_ids[0])
            project.status = "processing"
        else:
            project.status = "failed"
            project.error_message = result.get("message", "Generation failed")
        
        db.commit()
        return result
    
    @staticmethod
    async def check_status(project_id: str, db: Session) -> dict:
        """Check and update song generation status."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        if not project.task_id:
            return {"status": project.status}
        
        # Call Suno API
        result = await suno_service.get_task_status(int(project.task_id))
        
        # Update project
        project.status = result.get("status", project.status)
        
        if result.get("status") == "completed":
            project.music_url = result.get("audio_url")
            project.cover_url = result.get("cover_url")
            project.suno_id = result.get("custom_id")
            project.suno_title = result.get("title")
            project.duration = result.get("duration")
            project.points_cost = result.get("points_cost", 0)
        
        if result.get("error_msg"):
            project.error_message = result.get("error_msg")
            project.status = "failed"
        
        db.commit()
        return result
    
    @staticmethod
    def list_by_user(db: Session, user_id: str, limit: int = 50, offset: int = 0) -> List[Project]:
        """List user's projects."""
        return db.query(Project).filter(
            Project.user_id == user_id
        ).order_by(Project.created_at.desc()).offset(offset).limit(limit).all()
    
    @staticmethod
    def get(db: Session, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def delete(db: Session, project_id: str) -> bool:
        """Delete a project."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False
        
        db.delete(project)
        db.commit()
        return True


project_service = ProjectService()