"""Application entry point."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api import auth, voice, projects
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
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])


# ====================
# Health check
# ====================
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# ====================
# Frontend config
# ====================
DIST_FOLDER = Path(__file__).parent.parent / "frontend" / "dist"


@app.get("/")
async def root():
    """Serve frontend index."""
    if DIST_FOLDER.exists():
        index = DIST_FOLDER / "index.html"
        if index.exists():
            return HTMLResponse(index.read_text())
    return {"message": "Voca.ai API", "docs": "/docs"}


# ====================
# Voices storage (uploaded audio files)
# ====================
VOICE_FOLDER = Path("/home/ubuntu/voca.ai/backend/voices")
if VOICE_FOLDER.exists():
    app.mount("/voices", StaticFiles(directory=str(VOICE_FOLDER)), name="voices")


# ====================
# SPA fallback - must be LAST route
# ====================
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve frontend for any route not matched above."""
    # Filter out API routes
    if full_path.startswith("api/"):
        return {"detail": "Not Found"}
    
    if DIST_FOLDER.exists():
        index = DIST_FOLDER / "index.html"
        if index.exists():
            return HTMLResponse(index.read_text())
    return {"message": "Voca.ai API"}