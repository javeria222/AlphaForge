from pydantic import BaseModel
from typing import List, Optional


class DecisionEvidence(BaseModel):
    meeting_id: str
    timestamp: Optional[str] = None
    speaker: Optional[str] = None
    text: str


class DecisionResult(BaseModel):
    decision: str
    status: str
    evidence: List[DecisionEvidence]
