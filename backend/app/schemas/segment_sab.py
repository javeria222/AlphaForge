from pydantic import BaseModel

class SegmentBase(BaseModel):
    segment_id: str
    meeting_id: str
    speaker: str
    start_time: float
    end_time: float
    topic: str
    summary: str
    decision_text: str
    segment_text: str

    class Config:
        from_attributes = True