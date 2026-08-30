from sqlalchemy import Column, String, Integer, ForeignKey, Text
from app.database import Base


class Segment(Base):
    """
    Decision Segment model — the unit that everything downstream operates on.
    Contract §2.3 — segment_id format: "m{meetingNumber}_s{segmentNumber}" (e.g. "m2_s08")
    decision_text is nullable when segment is discussion but not an actual decision.
    """
    __tablename__ = "segments"

    segment_id = Column(String, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.meeting_id"), nullable=False, index=True)
    start_time = Column(Integer, nullable=False)  # seconds
    end_time = Column(Integer, nullable=False)  # seconds
    speaker = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    decision_text = Column(Text, nullable=True)  # null if not a decision
    segment_text = Column(Text, nullable=False)
