# Conversation Memory Voice Agent — API & Data Contract
### Shared Contract — Read This Before Writing Code

This is the single source of truth for every JSON shape, field name, and endpoint used across the project. If your module's input or output doesn't match a schema here, it's a bug in your module, not a variant to merge later. If a schema genuinely needs to change, change it here first and tell the team — don't just change your own module's output.

## 0. Ground Rules

- **All JSON keys are `snake_case`.** No `camelCase`, no `PascalCase`, anywhere in request or response bodies.
- **All timestamps are integer seconds (`start_time`, `end_time`) as the source of truth.** `mm:ss` strings (e.g. `"12:48"`) only appear in fields explicitly meant for display (like `evidence[].timestamp`) and are always derived from the integer, never hand-typed.
- **IDs are strings, not numbers**, even when they look numeric.
  - `meeting_id` format: `meeting_{n}` (e.g. `meeting_1`, `meeting_2`).
  - `segment_id` format: `m{meetingNumber}_s{segmentNumber}` (e.g. `m2_s08`).
- **Every list endpoint returns an object with a named array key**, never a bare JSON array — e.g. `{ "meetings": [...] }`, not `[...]`. This keeps room to add pagination fields later without a breaking change.
- **Optional fields are `null`, not omitted.** If a decision is unresolved, `decision_text` is `null` — the key is still present.
- Base URL for local dev: `http://localhost:8000/api`
- **Every request except `GET /health` must include `Authorization: Bearer <APP_API_KEY>`.** See §1.5.

## 1. Error Format

Every endpoint returns this shape on failure, with an appropriate HTTP status code.

```json
{
  "error": true,
  "code": "NOT_FOUND",
  "message": "Meeting 'meeting_9' does not exist."
}
```

| Code | HTTP Status | Meaning |
|---|---|---|
| `UNAUTHORIZED` | 401 | `Authorization` header missing, malformed, or the key is wrong. |
| `VALIDATION_ERROR` | 422 | Request body failed schema validation. |
| `NOT_FOUND` | 404 | Referenced meeting/segment does not exist. |
| `NOT_READY` | 409 | Requested resource exists but isn't processed yet (e.g. transcript requested before STT finished). |
| `UPSTREAM_ERROR` | 502 | AssemblyAI or the LLM API failed/timed out. |
| `INTERNAL_ERROR` | 500 | Unhandled server error. |

### 1.5 Authentication
Every route in the table below except `/health` is protected by a single shared API key, checked server-side by a FastAPI dependency. There are no per-user accounts in this MVP (see the functional doc, §16 and §20, for why).

**Request header, required on every call:**
```
Authorization: Bearer <APP_API_KEY>
```

**Failure response (any protected route, missing/wrong key):**
```json
{
  "error": true,
  "code": "UNAUTHORIZED",
  "message": "Missing or invalid API key."
}
```
HTTP status: `401`.

The key itself lives in `backend/.env` as `APP_API_KEY`. The frontend reads the same value from `frontend/.env` as `VITE_APP_API_KEY` and attaches the header in `src/api/client.ts` — every one of the endpoints below already assumes that header is present, so it isn't repeated in each example.

## 2. Core Data Models

### 2.1 Meeting
Owner: Person A. Represents one meeting's metadata and processing status.

```json
{
  "meeting_id": "meeting_2",
  "title": "Backend Sync - Database Discussion",
  "date": "2026-09-08",
  "audio_url": "/data/audio/meeting_2.wav",
  "duration_seconds": 900,
  "status": "ready"
}
```

`status` is one of: `"uploaded"` → `"transcribing"` → `"transcribed"` → `"segmented"` → `"ready"`, or `"failed"`. The frontend uses this to know whether it's safe to query a meeting yet.

### 2.2 Transcript Output
Owner: Person A. Raw AssemblyAI output, normalized to our shape. One object per meeting, containing all diarized utterances in order.

```json
{
  "meeting_id": "meeting_2",
  "utterances": [
    {
      "speaker": "Speaker A",
      "start_time": 748,
      "end_time": 775,
      "text": "Let's move from PostgreSQL to MongoDB."
    },
    {
      "speaker": "Speaker B",
      "start_time": 776,
      "end_time": 790,
      "text": "Agreed, MongoDB gives us more flexibility here."
    }
  ]
}
```

### 2.3 Decision Segment (Segmentation Output)
Owner: Person B. This is the unit everything downstream operates on — retrieval embeds these, reasoning reads these, the timeline UI renders these.

```json
{
  "segment_id": "m2_s08",
  "meeting_id": "meeting_2",
  "start_time": 748,
  "end_time": 775,
  "speaker": "Speaker A",
  "topic": "Database",
  "summary": "The team decided to move to MongoDB.",
  "decision_text": "PostgreSQL -> MongoDB",
  "segment_text": "Let's move from PostgreSQL to MongoDB."
}
```

- `decision_text` is `null` when the segment is discussion but not an actual decision/change (e.g. someone asking a question). Person B's LLM prompt should be explicit about this — not every segment is a decision.
- `topic` is free text but should stay consistent within one meeting series (e.g. always `"Database"`, not `"DB"` in one segment and `"Database choice"` in another) — Person C's retrieval quality depends on this.

**Segmentation endpoint response** (multiple segments for one meeting):
```json
{
  "meeting_id": "meeting_2",
  "segments": [ /* array of Decision Segment objects above */ ]
}
```

### 2.4 Retrieval Output
Owner: Person C. Response to a similarity search — top-K segments across ALL meetings, ranked by relevance.

```json
{
  "query": "What did we decide about the database?",
  "top_k": 5,
  "results": [
    {
      "segment_id": "m2_s08",
      "meeting_id": "meeting_2",
      "score": 0.91,
      "start_time": 748,
      "end_time": 775,
      "topic": "Database",
      "summary": "The team decided to move to MongoDB.",
      "decision_text": "PostgreSQL -> MongoDB",
      "segment_text": "Let's move from PostgreSQL to MongoDB."
    }
  ]
}
```

`score` is cosine similarity, `0.0`–`1.0`, always rounded to 2 decimal places. `results` is sorted descending by `score`.

### 2.5 Final Answer Output (Reasoning Output)
Owner: Person D. This is the payload the Voice Agent speaks from and the frontend renders — the most important contract in the project, since three roles (D, E, F) all consume it directly.

```json
{
  "question": "What did we finally decide about the database?",
  "status": "resolved",
  "final_decision": "PostgreSQL",
  "answer": "The final decision was PostgreSQL. The team initially proposed PostgreSQL in Meeting 1. In Meeting 2 at 12:48, the decision changed to MongoDB. In Meeting 3 at 18:20, it changed back to PostgreSQL.",
  "evidence": [
    {
      "segment_id": "m1_s03",
      "meeting_id": "meeting_1",
      "meeting_title": "Kickoff - Architecture Planning",
      "start_time": 500,
      "timestamp": "08:20",
      "change": "PostgreSQL proposed"
    },
    {
      "segment_id": "m2_s08",
      "meeting_id": "meeting_2",
      "meeting_title": "Backend Sync - Database Discussion",
      "start_time": 748,
      "timestamp": "12:48",
      "change": "PostgreSQL -> MongoDB"
    },
    {
      "segment_id": "m3_s05",
      "meeting_id": "meeting_3",
      "meeting_title": "Final Review",
      "start_time": 1100,
      "timestamp": "18:20",
      "change": "MongoDB -> PostgreSQL"
    }
  ]
}
```

- `status` is `"resolved"` or `"unresolved"`. If `"unresolved"`, `final_decision` is `null` and `answer` explicitly says the decision is unclear — **never fabricate a decision to fill the field.**
- `evidence` is always sorted chronologically by `start_time` ascending, across meetings — this is what the timeline UI iterates over directly to render each row and each `[▶]` click target.
- `answer` is the exact string sent to TTS. Keep it speakable — no markdown, no bullet characters.

## 3. Endpoints

| Method | Path | Auth Required | Owner | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | No | — | Liveness check. Returns `{ "status": "ok" }`. |
| `POST` | `/meetings` | Yes | A | Upload a new meeting (audio file + title). Returns a `Meeting` with `status: "uploaded"`. |
| `GET` | `/meetings` | Yes | A/F | List all meetings. Returns `{ "meetings": [Meeting, ...] }`. |
| `GET` | `/meetings/{meeting_id}` | Yes | A/F | Get one meeting's metadata + status. Returns a `Meeting`. |
| `GET` | `/meetings/{meeting_id}/transcript` | Yes | A/B | Get the raw transcript. Returns a `Transcript Output`. `404` if not yet transcribed. |
| `GET` | `/meetings/{meeting_id}/segments` | Yes | B/C | Get decision segments for one meeting. Returns `{ "meeting_id": ..., "segments": [...] }`. |
| `POST` | `/search` | Yes | C | Body: `{ "query": string, "top_k"?: int (default 5) }`. Returns a `Retrieval Output`. |
| `POST` | `/answer` | Yes | D | Body: `{ "question": string }`. Runs retrieval + reasoning internally. Returns a `Final Answer Output`. **This is the main endpoint the app is built around.** |
| `POST` | `/voice/tool/search_meeting_memory` | Yes | E | Tool-call endpoint the AssemblyAI Voice Agent invokes mid-conversation. Same request/response shape as `/answer` — kept as a separate route so voice-specific logging/latency handling doesn't touch the plain HTTP path. The Voice Agent's tool-calling config must be set up to send the `Authorization` header on this call. |

### 3.1 Voice Agent Tool Definition
Owner: Person E. This is the tool schema registered with the AssemblyAI Voice Agent — the contract between the voice layer and the backend.

```json
{
  "name": "search_meeting_memory",
  "description": "Search across all past meetings to answer a question about a decision, topic, or discussion.",
  "input_schema": {
    "type": "object",
    "properties": {
      "question": {
        "type": "string",
        "description": "The user's question, in natural language, exactly as asked."
      }
    },
    "required": ["question"]
  }
}
```

The tool's output, returned to the Voice Agent to speak, is the `Final Answer Output` shape from §2.5 — the agent should read `answer` aloud verbatim and can optionally reference `evidence` if asked a follow-up like "when did that change?"

## 4. End-to-End Field Flow

Use this to check your module isn't inventing a field name nobody downstream expects:

```
audio file
  → Meeting.audio_url
  → Transcript Output.utterances[] (speaker, start_time, end_time, text)
  → Decision Segment (segment_id, meeting_id, start_time, end_time, topic, summary, decision_text, segment_text)
  → Retrieval Output.results[] (adds: score)
  → Final Answer Output.evidence[] (adds: meeting_title, timestamp, change — reuses segment_id, meeting_id, start_time)
```

Every field that appears later in the pipeline keeps the exact same name it had earlier (`meeting_id`, `segment_id`, `start_time`) — nothing gets renamed midstream.

## 5. Open Questions For The Team

- **`top_k` default**: set to 5 here — confirm this is enough given only 2–3 meetings, or should it be lower (e.g. 3) so reasoning isn't diluted with weak matches?
- **Multi-turn voice follow-ups** (e.g. "when did that change?" after an answer): this contract treats each question as stateless. If the Voice Agent needs to remember the previous `evidence` to answer a follow-up without re-querying, that's a stateful addition not covered here — worth deciding before Person E builds the loop.
- **Auth key distribution**: `APP_API_KEY` needs to be generated once and shared with the whole team out-of-band (not committed to git). Decide who generates it and how it gets to everyone — e.g. a shared `.env.example` with a placeholder plus the real value dropped in the team chat/vault.
