from pydantic import BaseModel
from typing import Optional


class Utterance(BaseModel):
    """Single utterance in a transcript."""
    speaker: str
    start_time: int  # seconds
    end_time: int  # seconds
    text: str


class TranscriptOutput(BaseModel):
    """
    Response schema for GET /meetings/{meeting_id}/transcript per contract §2.2.
    Raw AssemblyAI output, normalized to our shape.
    """
    meeting_id: str
    utterances: list[Utterance]
