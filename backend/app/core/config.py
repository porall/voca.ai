"""FastAPI application configuration."""
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Voca.ai"
    debug: bool = False

# Database
    database_url: str = "sqlite:///./vocadb.sqlite"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30 * 24 * 60  # 30 days

    # CORS
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    # S3/OSS
    s3_bucket: str = "voca-ai-files"
    s3_region: str = "us-east-1"
    s3_access_key: str = ""
    s3_secret_key: str = ""

    # AI APIs
    suno_api_url: str = "https://api.suno.ai"
    reecho_api_url: str = "https://api.reecho.ai"
    reecho_api_key: str = ""


settings = Settings()