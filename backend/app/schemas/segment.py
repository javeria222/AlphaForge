from pydantic import BaseModel
from typing import Optional


class SegmentBase(BaseModel):
    """Base segment schema."""
    speaker: str
    start_time: int  # seconds
    end_time: int  # seconds
    topic: str
    summary: str
    decision_text: Optional[str] = None  # null if not a decision
    segment_text: str


class SegmentCreate(SegmentBase):
    """Schema for creating a new segment."""
    meeting_id: str


class Segment(SegmentBase):
    """
    Full Segment schema per contract §2.3.
    segment_id format: "m{meetingNumber}_s{segmentNumber}" (e.g. "m2_s08")
    """
    segment_id: str
    meeting_id: str

    class Config:
        from_attributes = True


class SegmentListResponse(BaseModel):
    """Response for GET /meetings/{meeting_id}/segments endpoint."""
    meeting_id: str
    segments: list[Segment]

