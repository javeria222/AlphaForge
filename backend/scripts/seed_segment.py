import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models.segment import Segment
from app.models.meeting import Meeting, MeetingStatus
from app.services.mock_data import get_mock_segments

def seed():
    db = SessionLocal()
    try:
        segments = get_mock_segments()  # embeddings already computed via encode() inside this call

        meeting_ids = {seg["meeting_id"] for seg in segments}
        for mid in meeting_ids:
            existing = db.query(Meeting).filter(Meeting.meeting_id == mid).first()
            if not existing:
                db.add(Meeting(
                    meeting_id=mid,
                    title=f"Mock {mid}",
                    date="2026-09-08",
                    audio_url=f"/data/audio/{mid}.wav",
                    duration_seconds=900,
                    status=MeetingStatus.ready,
                ))
        db.commit()

        for seg in segments:
            embedding = seg["embedding"]
            db.merge(Segment(
                segment_id=seg["segment_id"],
                meeting_id=seg["meeting_id"],
                start_time=seg["start_time"],
                end_time=seg["end_time"],
                speaker=seg["speaker"],
                topic=seg["topic"],
                summary=seg["summary"],
                decision_text=seg.get("decision_text"),
                segment_text=seg["segment_text"],
                embedding=embedding.tolist() if hasattr(embedding, "tolist") else list(embedding),
            ))
        db.commit()
        print(f"Seeded {len(segments)} segments.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()