"""
Part B: build contract-valid segments from the real transcripts, label them by hand,
embed segment_text, and load them into Postgres.

Run from backend/:   python scripts/seed_real_segments.py

Idempotent: deletes ALL segments of meeting_1..3 first (removes old mock rows), then inserts.
Fails loudly (non-zero exit, nothing written) if a label matches no utterance or several,
or if any utterance has no label.
"""
import json
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

MEETING_IDS = ["meeting_1", "meeting_2", "meeting_3"]
ALLOWED_TOPICS = {"Database", "Deployment", "Planning"}

# (distinctive substring of the utterance text, topic, summary, decision_text)
# decision_text is None unless the segment is an actual decision/change.
LABELS = {
    "meeting_1": [
        ("Welcome everyone", "Database", "The team opened the meeting to choose a database.", None),
        ("Our data is structured", "Database", "The team noted the data is structured and relational.", None),
        ("go with PostgreSQL", "Database", "The team proposed using PostgreSQL.", "Proposed PostgreSQL"),
        ("PostgreSQL gives us strong consistency", "Database", "The team agreed PostgreSQL fits for consistency and tooling.", None),
        ("Let's do Docker", "Deployment", "The team decided to deploy with Docker.", "Deploy via Docker"),
        ("Docker keeps our setup simple", "Deployment", "The team agreed Docker keeps the setup simple.", None),
        ("review the frontend design", "Planning", "The team will review the frontend design next week.", None),
    ],
    "meeting_2": [
        ("revisit the database decision", "Database", "The team reopened the database decision.", None),
        ("prototyping", "Database", "The transcript data was found to be loosely structured.", None),
        ("switch from PostgreSQL to MongoDB", "Database", "The team decided to move to MongoDB.", "PostgreSQL -> MongoDB"),
        ("MongoDB gives us more flexibility", "Database", "The team agreed MongoDB offers more flexibility.", None),
        ("the decision is MongoDB", "Database", "The team confirmed MongoDB and asked about deployment.", None),
        ("still using Docker", "Deployment", "The team confirmed Docker stays for deployment.", None),
        ("Great.", "Planning", "The meeting closed with a short acknowledgment.", None),
    ],
    "meeting_3": [
        ("lock the database choice", "Database", "The team needs to lock the database choice before the demo.", None),
        ("I tested MongoDB", "Database", "A team member began reporting on MongoDB testing.", None),
        ("relational after all", "Database", "The team noted the data is relational after all.", None),
        ("change back from MongoDB to PostgreSQL", "Database", "The team decided to revert to PostgreSQL.", "MongoDB -> PostgreSQL"),
        ("The final decision is PostgreSQL", "Database", "The team confirmed PostgreSQL as the final choice.", None),
        ("Deployment stays on Docker", "Deployment", "The team confirmed deployment stays on Docker.", None),
        ("finish the demo preparation", "Planning", "The team will finish the demo preparation.", None),
    ],
}


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def build_segments():
    """Pure file/label logic. No DB, no model. Raises SystemExit on any mismatch."""
    segments = []
    for meeting_id in MEETING_IDS:
        path = f"data/transcripts/{meeting_id}.json"
        try:
            with open(path, encoding="utf-8") as f:
                utterances = json.load(f)
        except FileNotFoundError:
            fail(f"{path} not found (run from backend/).")

        labels = LABELS[meeting_id]
        matched = {}  # utterance index -> label
        for label in labels:
            needle = label[0]
            hits = [i for i, u in enumerate(utterances) if needle in u["text"]]
            if len(hits) != 1:
                fail(f"{meeting_id}: label {needle!r} matched {len(hits)} utterances (need exactly 1).")
            if hits[0] in matched:
                fail(f"{meeting_id}: utterance {hits[0]} matched by two labels ({needle!r}).")
            matched[hits[0]] = label

        unlabeled = [i for i in range(len(utterances)) if i not in matched]
        if unlabeled:
            fail(f"{meeting_id}: utterances without a label: {unlabeled}: "
                 + "; ".join(utterances[i]["text"] for i in unlabeled))

        num = int(re.search(r"(\d+)$", meeting_id).group(1))
        for i, u in enumerate(utterances):
            _, topic, summary, decision = matched[i]
            if topic not in ALLOWED_TOPICS:
                fail(f"{meeting_id}: bad topic {topic!r}.")
            if u["meeting_id"] != meeting_id:
                fail(f"{path}: utterance {i} has meeting_id {u['meeting_id']!r}.")
            start, end = int(u["start_time"]), int(u["end_time"])
            if end < start:
                fail(f"{meeting_id}: utterance {i} end_time < start_time.")
            segments.append({
                "segment_id": f"m{num}_s{i + 1:02d}",
                "meeting_id": meeting_id,
                "start_time": start,
                "end_time": end,
                "speaker": u["speaker"],
                "topic": topic,
                "summary": summary,
                "decision_text": decision,
                "segment_text": u["text"],
            })
    return segments


def main():
    segments = build_segments()  # validate everything BEFORE touching the DB or loading the model

    from app.database import SessionLocal
    from app.models.segment import Segment
    from app.models.meeting import Meeting, MeetingStatus
    from app.services.embeddings import embeddings_service  # downloads model on first run

    db = SessionLocal()
    try:
        found = {m.meeting_id for m in db.query(Meeting).filter(Meeting.meeting_id.in_(MEETING_IDS)).all()}
        missing = set(MEETING_IDS) - found
        if missing:
            fail(f"meetings missing in DB (run register_meetings.py first): {sorted(missing)}")

        rows = []
        for s in segments:
            emb = embeddings_service.encode(s["segment_text"])
            s["embedding"] = emb.tolist() if hasattr(emb, "tolist") else list(emb)
            rows.append(Segment(**s))

        db.query(Segment).filter(Segment.meeting_id.in_(MEETING_IDS)).delete(synchronize_session=False)
        db.flush()
        db.add_all(rows)
        db.query(Meeting).filter(Meeting.meeting_id.in_(MEETING_IDS)).update(
            {"status": MeetingStatus.ready}, synchronize_session=False
        )
        db.commit()
    except SystemExit:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    print(f"{'segment_id':<10} {'meeting':<10} {'time':<9} {'topic':<11} {'decision_text':<24} text")
    print("-" * 110)
    for s in segments:
        span = f"{s['start_time']}-{s['end_time']}"
        print(f"{s['segment_id']:<10} {s['meeting_id']:<10} {span:<9} {s['topic']:<11} "
              f"{(s['decision_text'] or '-'):<24} {s['segment_text'][:50]}")
    print(f"\nInserted {len(segments)} segments; meetings set to ready.")


if __name__ == "__main__":
    main()