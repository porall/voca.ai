"""Database models for Voca.ai."""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(100))
    avatar_url = Column(Text)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Voice(Base):
    """Voice clone model."""
    __tablename__ = "voices"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    audio_url = Column(Text, nullable=False)
    duration_secs = Column(Float)
    is_default = Column(Boolean, default=False)
    status = Column(String(20), default="pending")  # pending, ready, failed
    created_at = Column(DateTime, default=datetime.utcnow)


class Project(Base):
    """Project model."""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    lyrics = Column(Text)
    music_genre = Column(String(50))
    style = Column(String(100))
    voice_id = Column(UUID(as_uuid=True), ForeignKey("voices.id"))
    music_url = Column(Text)  # Suno generated
    vocal_url = Column(Text)  # Reecho synthesized
    final_url = Column(Text)  # Merged final
    status = Column(String(20), default="draft")  # draft, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)