# backend/app/services/mock_data.py

from app.services.embeddings import embeddings_service

mock_segments = [
    {
        "segment_id": "m1_s01",
        "meeting_id": "meeting_1",
        "start_time": 500,
        "end_time": 520,
        "speaker": "Speaker A",
        "topic": "Database",
        "summary": "The team proposed using PostgreSQL.",
        "decision_text": "Proposed PostgreSQL",
        "segment_text": "I think we should go with PostgreSQL for this."
    },
    {
        "segment_id": "m1_s02",
        "meeting_id": "meeting_1",
        "start_time": 610,
        "end_time": 640,
        "speaker": "Speaker B",
        "topic": "Deployment",
        "summary": "Discussion of hosting options, no decision made yet.",
        "decision_text": None,
        "segment_text": "Should we look at Docker or just deploy on a VPS directly? Let's revisit next week."
    },
    {
        "segment_id": "m1_s03",
        "meeting_id": "meeting_1",
        "start_time": 700,
        "end_time": 730,
        "speaker": "Speaker A",
        "topic": "Timeline",
        "summary": "Team agreed on a two-week sprint for the MVP.",
        "decision_text": "Two-week sprint for MVP",
        "segment_text": "Let's aim for a two-week sprint to get the MVP out."
    },
    {
        "segment_id": "m2_s01",
        "meeting_id": "meeting_2",
        "start_time": 748,
        "end_time": 775,
        "speaker": "Speaker A",
        "topic": "Database",
        "summary": "The team decided to move to MongoDB.",
        "decision_text": "PostgreSQL -> MongoDB",
        "segment_text": "Let's move from PostgreSQL to MongoDB."
    },
    {
        "segment_id": "m2_s02",
        "meeting_id": "meeting_2",
        "start_time": 776,
        "end_time": 790,
        "speaker": "Speaker B",
        "topic": "Database",
        "summary": "Agreement on the reasoning behind the MongoDB switch.",
        "decision_text": None,
        "segment_text": "Agreed, MongoDB gives us more flexibility here."
    },
    {
        "segment_id": "m2_s03",
        "meeting_id": "meeting_2",
        "start_time": 900,
        "end_time": 940,
        "speaker": "Speaker A",
        "topic": "Deployment",
        "summary": "Team decided to use Docker for deployment.",
        "decision_text": "Deploy via Docker",
        "segment_text": "Let's containerize this with Docker so it's consistent across environments."
    },
    {
        "segment_id": "m3_s01",
        "meeting_id": "meeting_3",
        "start_time": 1100,
        "end_time": 1130,
        "speaker": "Speaker B",
        "topic": "Database",
        "summary": "Final decision reverted back to PostgreSQL.",
        "decision_text": "MongoDB -> PostgreSQL",
        "segment_text": "After testing, we're going back to PostgreSQL — it fits our query patterns better."
    },
]

_embeddings_computed = False

def get_mock_segments():
    global _embeddings_computed
    if not _embeddings_computed:
        for seg in mock_segments:                       # deleted: embeddings_service = EmbeddingsService()
            seg["embedding"] = embeddings_service.encode(seg["segment_text"])
        _embeddings_computed = True
    return mock_segments