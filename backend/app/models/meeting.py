from sqlalchemy import Column, String, DateTime, Integer, Enum
from datetime import datetime
from app.database import Base
import enum


class MeetingStatus(str, enum.Enum):
    """Meeting processing status enum per contract §2.1."""
    uploaded = "uploaded"
    transcribing = "transcribing"
    transcribed = "transcribed"
    segmented = "segmented"
    ready = "ready"
    failed = "failed"


class Meeting(Base):
    """
    Meeting model representing one meeting's metadata and processing status.
    Contract §2.1 — meeting_id format: "meeting_{n}" (e.g. "meeting_1")
    """
    __tablename__ = "meetings"

    meeting_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)  # ISO format: "2026-09-08"
    audio_url = Column(String, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    status = Column(Enum(MeetingStatus), default=MeetingStatus.uploaded, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
