"""Project/Song service for managing songs."""
from typing import List, Optional
import uuid
import os
import subprocess

from sqlalchemy.orm import Session

from app.models.db import Project
from app.services.suno import suno_service
from app.services.cosyvoice import cosyvoice_service


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
            
            # 如果选择了声音（Suno生成了伴奏），则合成人声并合并
            if project.voice_id and project.lyrics and project.music_url:
                await ProjectService._synthesize_vocal(project, db)
        
        if result.get("error_msg"):
            project.error_message = result.get("error_msg")
            project.status = "failed"

        db.commit()
        return result
    
    @staticmethod
    async def _synthesize_vocal(project: Project, db: Session) -> dict:
        """Synthesize vocal track with CosyVoice and merge with music."""
        try:
            # 调用 CosyVoice 合成人声
            vocal_result = await cosyvoice_service.synthesize(
                text=project.lyrics,
                voice_id=project.voice_id,
            )
            
            vocal_url = vocal_result.get("audio_url")
            if vocal_url:
                project.vocal_url = vocal_url
                
                # 下载两个音频文件并合并
                final_url = await project_service._merge_audio(
                    vocal_url, project.music_url, project.id
                )
                if final_url:
                    project.final_url = final_url
                    project.status = "completed"
        except Exception as e:
            # 如果合成失败，至少保留 instrumental
            project.error_message = f"Vocal synthesis failed: {str(e)}"
        
        db.commit()
        return {}
    
    @staticmethod
    async def _merge_audio(vocal_url: str, music_url: str, project_id: str) -> Optional[str]:
        """Merge vocal and music tracks."""
        output_dir = "/home/ubuntu/voca.ai/backend/voices"
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"{project_id}_final.mp3")
        
        # 如果 URL 是本地路径，下载/读取
        try:
            # 构建完整 URL（假设 music_url 是相对路径）
            if not music_url.startswith("http"):
                music_full_url = f"http://localhost:8000{music_url}"
            else:
                music_full_url = music_url
            
            # 简单合并（用一个简单的混音命令）
            # 实际生产中需要下载两个文件然后用 ffmpeg 合并
            cmd = [
                "ffmpeg", "-y",
                "-i", music_full_url,
                "-i", vocal_url,
                "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first",
                "-shortest",
                output_file
            ]
            subprocess.run(cmd, capture_output=True, timeout=60)
            
            if os.path.exists(output_file):
                return f"/voices/{os.path.basename(output_file)}"
        except Exception as e:
            print(f"Audio merge failed: {e}")
        
        return None
    
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