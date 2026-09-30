import os
import tempfile

import assemblyai as aai

from app.config import settings


class TranscriptionError(Exception):
    pass


def transcribe_bytes(data: bytes) -> str:
    aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
        f.write(data)
        path = f.name
    try:
        transcript = aai.Transcriber().transcribe(path, config=aai.TranscriptionConfig())
    finally:
        os.remove(path)
    if transcript.status == aai.TranscriptStatus.error:
        raise TranscriptionError(transcript.error or "Transcription failed")
    return (transcript.text or "").strip()