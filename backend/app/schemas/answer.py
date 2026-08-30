from pydantic import BaseModel
from typing import Optional, Literal


class Evidence(BaseModel):
    """Single piece of evidence in final answer."""
    segment_id: str
    meeting_id: str
    meeting_title: str
    start_time: int  # seconds, source of truth
    timestamp: str  # mm:ss format, derived from start_time for display
    change: str


class FinalAnswerOutput(BaseModel):
    """
    Response schema for POST /answer and POST /voice/tool/search_meeting_memory
    per contract §2.5.
    This is the main payload the Voice Agent speaks from and frontend renders.
    """
    question: str
    status: Literal["resolved", "unresolved"]
    final_decision: Optional[str] = None  # null if unresolved
    answer: str  # Exact string sent to TTS, speakable, no markdown
    evidence: list[Evidence]  # Sorted chronologically by start_time ascending


class AnswerQuery(BaseModel):
    """Request schema for POST /answer and /voice/tool/search_meeting_memory."""
    question: str
