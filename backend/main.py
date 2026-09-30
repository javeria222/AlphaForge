from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import meetings, search, voice
from pathlib import Path
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Conversation Memory Voice Agent API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your actual Vite dev origin, not "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint (no auth required per contract §3)
@app.get("/health")
async def health():
    """Liveness check. No authentication required."""
    return {"status": "ok"}


# Include API routers
# Base path: /api (set in Pydantic/FastAPI configuration if needed)
app.include_router(meetings.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(voice.router, prefix="/api")

AUDIO_DIR = Path(__file__).parent / "data" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)  # Creates directory if it doesn't exist
app.mount("/data/audio", StaticFiles(directory=AUDIO_DIR), name="audio")
