from pydantic import BaseModel
from typing import Optional
from app.models.meeting import MeetingStatus


class MeetingBase(BaseModel):
    """Base meeting schema."""
    title: str
    date: str  # ISO format: "2026-09-08"
    audio_url: str
    duration_seconds: int


class MeetingCreate(MeetingBase):
    """Schema for creating a new meeting."""
    pass


class Meeting(MeetingBase):
    """
    Full Meeting schema per contract §2.1.
    meeting_id format: "meeting_{n}" (e.g. "meeting_1")
    """
    meeting_id: str
    status: MeetingStatus

    class Config:
        from_attributes = True


class MeetingListResponse(BaseModel):
    """Response for GET /meetings endpoint."""
    meetings: list[Meeting]

