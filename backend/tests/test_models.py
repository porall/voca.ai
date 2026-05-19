"""Test for database models."""
import pytest
from datetime import datetime
from uuid import uuid4

from app.models.db import User, Voice, Project


def test_user_model_fields():
    """User model should have expected fields."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        nickname="Test User",
        is_premium=False,
        created_at=datetime.utcnow()
    )
    
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_password"
    assert user.nickname == "Test User"
    assert user.is_premium == False


def test_voice_model_fields():
    """Voice model should have expected fields."""
    voice = Voice(
        id=uuid4(),
        user_id=uuid4(),
        name="My Voice",
        audio_url="https://example.com/voice.mp3",
        duration_secs=30.0,
        is_default=True,
        status="ready",
        created_at=datetime.utcnow()
    )
    
    assert voice.name == "My Voice"
    assert voice.duration_secs == 30.0
    assert voice.status == "ready"


def test_project_model_fields():
    """Project model should have expected fields."""
    project = Project(
        id=uuid4(),
        user_id=uuid4(),
        name="My Song",
        lyrics="Hello world",
        music_genre="pop",
        style="upbeat",
        status="draft",
        created_at=datetime.utcnow()
    )
    
    assert project.name == "My Song"
    assert project.lyrics == "Hello world"
    assert project.music_genre == "pop"
    assert project.status == "draft"