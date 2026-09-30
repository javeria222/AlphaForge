from pydantic import BaseModel
from typing import List, Optional

class EvidenceItem(BaseModel):
    meeting: str
    timestamp: str
    change: str

class FinalDecisionResponse(BaseModel):
    final_decision: str
    answer: str
    evidence: List[EvidenceItem]