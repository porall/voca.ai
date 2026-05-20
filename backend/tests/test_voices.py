"""Test for Voice API."""
import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.db import Base, get_db, User, Voice
from app.core.config import settings


# Test database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """Create test client."""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(client):
    """Create a test user."""
    # Use auth API to create user
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123", "nickname": "Test User"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def auth_token(client, test_user):
    """Get auth token."""
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_list_voices_empty(client, auth_token):
    """Should return empty list when no voices."""
    response = client.get(
        "/api/voices",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_upload_voice_requires_auth(client):
    """Should reject upload without auth."""
    response = client.post("/api/voices/upload")
    assert response.status_code == 401


def test_upload_voice_requires_file(client, auth_token):
    """Should reject upload without file."""
    response = client.post(
        "/api/voices/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 422  # Missing file


def test_upload_voice_with_file(client, auth_token):
    """Should accept audio file upload."""
    # Create a small MP3 file in memory
    audio_content = b"FAKE_MP3_CONTENT"
    files = {"file": ("test_voice.mp3", io.BytesIO(audio_content), "audio/mpeg")}
    data = {"name": "My Voice"}
    
    response = client.post(
        "/api/voices/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files=files,
        data=data,
    )
    
    # Should return voice info (status may be pending)
    assert response.status_code == 201
    result = response.json()
    assert "id" in result
    assert result["name"] == "My Voice"


def test_list_voices_after_upload(client, auth_token):
    """Should return uploaded voices."""
    # Upload first
    audio_content = b"FAKE_MP3_CONTENT"
    files = {"file": ("test_voice.mp3", io.BytesIO(audio_content), "audio/mpeg")}
    client.post(
        "/api/voices/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files=files,
        data={"name": "My Voice"},
    )
    
    # Then list
    response = client.get(
        "/api/voices",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    
    assert response.status_code == 200
    voices = response.json()
    assert len(voices) == 1
    assert voices[0]["name"] == "My Voice"


def test_delete_voice(client, auth_token):
    """Should delete a voice."""
    # Upload first
    audio_content = b"FAKE_MP3_CONTENT"
    files = {"file": ("test_voice.mp3", io.BytesIO(audio_content), "audio/mpeg")}
    create_response = client.post(
        "/api/voices/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files=files,
        data={"name": "My Voice"},
    )
    voice_id = create_response.json()["id"]
    
    # Delete
    response = client.delete(
        f"/api/voices/{voice_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    
    assert response.status_code == 204


def test_cannot_delete_other_users_voice(client, auth_token):
    """Should not delete another user's voice."""
    # Create another user and their voice
    client.post(
        "/api/auth/register",
        json={"email": "other@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/api/auth/login",
        data={"username": "other@example.com", "password": "password123"},
    )
    other_token = login_response.json()["access_token"]
    
    audio_content = b"FAKE_MP3_CONTENT"
    files = {"file": ("voice.mp3", io.BytesIO(audio_content), "audio/mpeg")}
    voice_response = client.post(
        "/api/voices/upload",
        headers={"Authorization": f"Bearer {other_token}"},
        files=files,
        data={"name": "Other Voice"},
    )
    other_voice_id = voice_response.json()["id"]
    
    # Try to delete with our token
    response = client.delete(
        f"/api/voices/{other_voice_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    
    assert response.status_code == 404  # Not found (doesn't exist for this user)