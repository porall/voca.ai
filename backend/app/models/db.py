"""Database models for Voca.ai."""
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.core.config import settings

Base = declarative_base()


# Database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    poolclass=StaticPool if settings.database_url.startswith("sqlite") else None,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(100))
    avatar_url = Column(Text)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    voices = relationship("Voice", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")


class Voice(Base):
    """Voice clone model."""
    __tablename__ = "voices"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    audio_url = Column(Text, nullable=False)
    duration_secs = Column(Float)
    is_default = Column(Boolean, default=False)
    status = Column(String(20), default="pending")  # pending, ready, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="voices")


class Project(Base):
    """Project/Song model."""
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)  # 项目名/歌曲名
    
    # Song creation params
    gpt_description = Column(Text)  # AI描述 prompt
    lyrics = Column(Text)  # 自定义歌词
    music_genre = Column(String(50))  # 风格标签
    style = Column(String(100))  # 歌手风格预设
    
    # Voice
    voice_id = Column(String(36), ForeignKey("voices.id"))  # 克隆声音ID
    
    # Generation
    task_id = Column(String(50))  # Suno任务ID
    suno_title = Column(String(200))  # Suno返回的歌曲名
    suno_id = Column(String(36))  # Suno歌曲ID(custom_id)
    mv = Column(String(20), default="chirp-fenix")  # 模型版本
    duration = Column(Integer)  # 时长(秒)
    
    # URLs
    music_url = Column(Text)  # Suno生成的AI歌曲
    cover_url = Column(Text)  # 封面图
    vocal_url = Column(Text)  # Reecho合成的人声
    final_url = Column(Text)  # 合并后的成品
    
    # Status
    status = Column(String(20), default="draft")  # draft-草稿, pending-等待生成, processing-生成中, completed-完成, failed-失败
    error_message = Column(Text)  # 错误信息
    points_cost = Column(Integer, default=0)  # 消耗积分
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")