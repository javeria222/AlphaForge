from pydantic import BaseModel
from typing import Optional


class RetrievalQuery(BaseModel):
    """Request schema for POST /search endpoint per contract §3."""
    query: str
    top_k: int = 5  # default 5


class RetrievalResult(BaseModel):
    """Single result in retrieval output."""
    segment_id: str
    meeting_id: str
    score: float  # cosine similarity, 0.0-1.0, rounded to 2 decimals
    start_time: int  # seconds
    end_time: int  # seconds
    topic: str
    summary: str
    decision_text: Optional[str] = None
    segment_text: str


class RetrievalOutput(BaseModel):
    """
    Response schema for POST /search endpoint per contract §2.4.
    Results are sorted descending by score.
    """
    query: str
    top_k: int
    results: list[RetrievalResult]

