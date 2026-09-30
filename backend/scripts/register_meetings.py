import json, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal
from app.models.meeting import Meeting, MeetingStatus

MEETINGS = [
    ("meeting_1", "Kickoff - Architecture Planning", "2026-09-01"),
    ("meeting_2", "Backend Sync - Database Discussion", "2026-09-08"),
    ("meeting_3", "Final Review", "2026-09-15"),
]

db = SessionLocal()
try:
    for meeting_id, title, date in MEETINGS:
        with open(f"data/transcripts/{meeting_id}.json", encoding="utf-8") as f:
            utterances = json.load(f)
        duration = max(u["end_time"] for u in utterances) + 1
        db.merge(Meeting(
            meeting_id=meeting_id, title=title, date=date,
            audio_url=f"/data/audio/{meeting_id}.mp3",
            duration_seconds=duration, status=MeetingStatus.transcribed,
        ))
        print(meeting_id, len(utterances), "utterances,", duration, "s")
    db.commit()
finally:
    db.close()