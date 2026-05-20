"""Application entry point."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api import auth, voice, project
from app.models.db import init_db

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====================
# API routers FIRST
# ====================
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(voice.router, prefix="/api/voices", tags=["voices"])
app.include_router(project.router, prefix="/api/projects", tags=["projects"])


# ====================
# Health check
# ====================
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# ====================
# Frontend config
# ====================
STATIC_FOLDER = Path(__file__).parent / "static"


@app.get("/")
async def root():
    """Serve frontend index."""
    if STATIC_FOLDER.exists():
        index = STATIC_FOLDER / "index.html"
        if index.exists():
            return HTMLResponse(index.read_text())
    return {"message": "Voca.ai API", "docs": "/docs"}


# ====================
# Voices storage (uploaded audio files)
# ====================
VOICE_FOLDER = Path("/home/ubuntu/voca.ai/backend/voices")
if VOICE_FOLDER.exists():
    app.mount("/voices", StaticFiles(directory=str(VOICE_FOLDER)))


# ====================
# Static files for SPA assets
# ====================
if STATIC_FOLDER.exists() and (STATIC_FOLDER / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_FOLDER / "assets")))


# ====================
# SPA fallback - must be LAST route
# ====================
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve frontend for any route not matched above."""
    # Filter out API routes (exact matches for known API prefixes)
    api_prefixes = ["/api/auth", "/api/voices", "/api/projects"]
    if any(full_path.startswith(prefix) for prefix in api_prefixes):
        return {"detail": "Not Found"}
    # Filter out static assets
    if full_path.startswith("assets/") or full_path == "favicon.svg":
        return {"detail": "Not Found"}
    # Serve index.html for SPA routes (song-create, task, etc)
    if STATIC_FOLDER.exists():
        index = STATIC_FOLDER / "index.html"
        if index.exists():
            return HTMLResponse(index.read_text())
    return {"message": "Voca.ai API"}