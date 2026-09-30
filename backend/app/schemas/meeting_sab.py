from pydantic import BaseModel
from typing import List

class MeetingBase(BaseModel):
    id: str
    title: str

    class Config:
        from_attributes = True