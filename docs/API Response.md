# API Response Documentation — Retrieval Module (Person C)

Scope: this document covers only the endpoints owned or co-owned by Person C
(Retrieval/RAG), per the AlphaForge data contract §3:

- `POST /search` — owned by Person C
- `GET /meetings/{meeting_id}/segments` — co-owned by Person B/C

`POST /answer`, the meeting CRUD routes, and the voice tool endpoint belong to
other team members and are intentionally out of scope here.

**Base URL:** `http://localhost:8000/api`

**Auth:** every request below requires
`Authorization: Bearer <APP_API_KEY>`. The key is omitted from the examples
below and replaced with a placeholder — do not commit a real key into this
file.

---

## 1. `POST /search`

Semantic search across all meetings for relevant decision segments.

### Request

```
POST /api/search
Authorization: Bearer <APP_API_KEY>
Content-Type: application/json
```

```json
{
  "query": "what did we decide about the database",
  "top_k": 3
}
```

### Successful response — 200 OK

```json
{
  "query": "what did we decide about the database",
  "top_k": 3,
  "results": [
    {
      "segment_id": "m2_s01",
      "meeting_id": "meeting_2",
      "score": 0.49,
      "start_time": 748,
      "end_time": 775,
      "topic": "Database",
      "summary": "The team decided to move to MongoDB.",
      "decision_text": "PostgreSQL -> MongoDB",
      "segment_text": "Let's move from PostgreSQL to MongoDB."
    },
    {
      "segment_id": "m1_s01",
      "meeting_id": "meeting_1",
      "score": 0.43,
      "start_time": 500,
      "end_time": 520,
      "topic": "Database",
      "summary": "The team proposed using PostgreSQL.",
      "decision_text": "Proposed PostgreSQL",
      "segment_text": "I think we should go with PostgreSQL for this."
    },
    {
      "segment_id": "m2_s02",
      "meeting_id": "meeting_2",
      "score": 0.43,
      "start_time": 776,
      "end_time": 790,
      "topic": "Database",
      "summary": "Agreement on the reasoning behind the MongoDB switch.",
      "decision_text": null,
      "segment_text": "Agreed, MongoDB gives us more flexibility here."
    }
  ]
}
```

Notes on this result: `m2_s01` ranks highest because it has a non-null
`decision_text`, which applies the contract's +0.1 similarity boost (capped
at 1.0). `m2_s02` has an identical raw topic match but no decision boost, so
it ranks below both decision segments despite being conversationally
adjacent to `m2_s01`. Results are verified sourced from Postgres, not the
mock in-memory fixture — confirmed by a full server restart between seed and
query with identical results returned.

### Error response — 422 Unprocessable Content

Returned when the request body isn't valid JSON (e.g. malformed quoting).

```json
{
  "detail": [
    {
      "type": "json_invalid",
      "loc": ["body", 0],
      "msg": "JSON decode error",
      "input": {},
      "ctx": {
        "error": "Expecting value"
      }
    }
  ]
}
```

---

## 2. `GET /meetings/{meeting_id}/segments`

Returns all decision segments for one meeting.

### Request

```
GET /api/meetings/meeting_2/segments
Authorization: Bearer <APP_API_KEY>
```

### Successful response — 200 OK

```json
{
  "meeting_id": "meeting_2",
  "segments": [
    {
      "speaker": "Speaker A",
      "start_time": 748,
      "end_time": 775,
      "topic": "Database",
      "summary": "The team decided to move to MongoDB.",
      "decision_text": "PostgreSQL -> MongoDB",
      "segment_text": "Let's move from PostgreSQL to MongoDB.",
      "segment_id": "m2_s01",
      "meeting_id": "meeting_2"
    },
    {
      "speaker": "Speaker B",
      "start_time": 776,
      "end_time": 790,
      "topic": "Database",
      "summary": "Agreement on the reasoning behind the MongoDB switch.",
      "decision_text": null,
      "segment_text": "Agreed, MongoDB gives us more flexibility here.",
      "segment_id": "m2_s02",
      "meeting_id": "meeting_2"
    },
    {
      "speaker": "Speaker A",
      "start_time": 900,
      "end_time": 940,
      "topic": "Deployment",
      "summary": "Team decided to use Docker for deployment.",
      "decision_text": "Deploy via Docker",
      "segment_text": "Let's containerize this with Docker so it's consistent across environments.",
      "segment_id": "m2_s03",
      "meeting_id": "meeting_2"
    }
  ]
}
```

### Error response — 404 Not Found

Returned when no meeting exists with the given `meeting_id`.

**Request:** `GET /api/meetings/meeting_22/segments`

```json
{
  "detail": {
    "error": true,
    "code": "NOT_FOUND",
    "message": "Meeting 'meeting_22' not found"
  }
}
```

### Error response — 409 Conflict (NOT_READY)

Returned when the meeting exists but its `status` is not `ready` (e.g. still
transcribing or segmenting).

**Request:** `GET /api/meetings/meeting_test_notready/segments`

```json
{
  "detail": {
    "error": true,
    "code": "NOT_READY",
    "message": "Meeting 'meeting_test_notready' is not ready yet (status: transcribing)"
  }
}
```

---

## Known limitation as of this snapshot

All data above comes from the seeded mock fixture (7 segments across 3
meetings), not real meeting audio — ingestion (Person A) and segmentation
(Person B) have not shipped real data yet. Retrieval and the segments
endpoint are both verified working against real Postgres rows; they will
work identically against real segments once those land, provided each real
segment's `embedding` column is populated at creation time (in progress,
owned by Person B).
