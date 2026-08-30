# Conversation Memory Voice Agent
### Functional & Technical Project Document

Ask your past meetings anything by voice, understand how decisions changed, and jump to the exact evidence.

| Document Area | Details |
|---|---|
| Project Type | AI / Generative AI / RAG / Voice Agent |
| Recommended Voice Approach | AssemblyAI Voice Agent API — Part 1 (Managed) |
| Backend | Python + FastAPI |
| Frontend | React + Vite + TypeScript |
| Database | PostgreSQL |
| RAG | Embeddings + in-memory cosine similarity |
| MVP | 2–3 scripted meetings, 10–15 minutes each |
| Main Output | Spoken answer + decision history + meeting/timestamp evidence |

## 1. Project Title
Conversation Memory Voice Agent

## 2. Project Description
Conversation Memory Voice Agent is an AI-powered meeting-memory system. A user can ask a question naturally by voice, such as "What did we finally decide about the database?" The system searches across multiple meeting transcripts, retrieves the most relevant parts, and uses an LLM to understand the discussion and decision history.

Instead of only returning a text search result, the system gives a final answer back in speech. It also shows evidence such as the meeting number, timestamp, speaker, and what changed. The user can click that evidence and jump directly to the relevant moment in the meeting recording.

## 3. Problem We Are Solving
Teams often have many meetings where the same topic is discussed again and decisions change over time. Finding the final decision manually requires opening several recordings or transcripts and comparing them.

This project solves that problem by creating a searchable voice memory for meetings.
- Search multiple meetings instead of one transcript at a time.
- Understand the meaning of discussions using semantic retrieval.
- Track how a decision changed from one meeting to another.
- Give a final answer instead of simply returning raw transcript text.
- Provide evidence with exact timestamps.
- Allow the user to jump directly to the original audio.

## 4. Overall Functionality — Simple Explanation
The complete system works in two main stages: first, it builds meeting memory; second, it uses that memory to answer voice questions.

**STAGE 1 — BUILD MEETING MEMORY**
```
Meeting Audio
 ↓
AssemblyAI
 ↓
Transcript + Speaker Labels + Timestamps
 ↓
LLM Segment Extraction
 ↓
Topic / Decision Segments
 ↓
Embeddings
 ↓
PostgreSQL + In-Memory Retrieval Store
```

**STAGE 2 — ANSWER A VOICE QUESTION**
```
User asks a question by voice
 ↓
AssemblyAI Voice Agent
 ↓
Speech-to-Text
 ↓
Search Memory Tool
 ↓
Embedding + Cosine Similarity
 ↓
Top-K Relevant Segments from ALL Meetings
 ↓
LLM Decision Reasoning
 ↓
Final Answer + Evidence
 ↓
TTS / Spoken Response
 ↓
Frontend Timeline + Audio Jump
```

## 5. Core MVP Functionalities
| # | Functionality | Clear Function |
|---|---|---|
| 1 | Mock Meeting Corpus | Create 2–3 scripted audio meetings, around 10–15 minutes each, on the same evolving topic. |
| 2 | STT + Speaker Diarization | Use AssemblyAI to convert each meeting into transcript text with speaker labels and timestamps. |
| 3 | Segment Extraction | Use an LLM to divide each transcript into useful topic/decision segments, each with a timestamp and short summary. |
| 4 | Lightweight RAG Retrieval | Embed every segment and use in-memory cosine similarity to find the top relevant segments across all meetings. |
| 5 | Decision Tracking | Compare retrieved segments in chronological order and identify what was decided, changed, and finally agreed. |
| 6 | Voice Query Loop | User asks a question by voice; the voice agent calls the retrieval/reasoning tools and speaks the final answer. |
| 7 | Minimal Timeline UI | Show important segments across meetings in order. Each item can be clicked to jump to that audio moment. |

## 6. Example — How the Project Actually Works
Assume the team discusses a database in three meetings.

- **Meeting 1 — 08:20**: Team proposes PostgreSQL.
- **Meeting 2 — 12:48**: Team changes the decision: PostgreSQL → MongoDB.
- **Meeting 3 — 18:20**: Team changes the decision again: MongoDB → PostgreSQL.

User asks by voice: *"What did we finally decide about the database?"*

The retrieval system searches all three meetings. It finds the database-related segments. The reasoning LLM reads those segments in chronological order.

The final answer could be:
> "The final decision was PostgreSQL. The team initially proposed PostgreSQL in Meeting 1. In Meeting 2 at 12:48, the decision changed to MongoDB. In Meeting 3 at 18:20, it changed back to PostgreSQL."

The UI then shows:
```
Meeting 1 — 08:20 — PostgreSQL proposed [▶]
Meeting 2 — 12:48 — Changed to MongoDB [▶]
Meeting 3 — 18:20 — Changed to PostgreSQL [▶]
```
When the user clicks the second item, the audio player jumps directly to 12:48.

## 7. Decision Tracking Logic
Decision tracking is the main feature that makes this more than a normal transcript search.
- Retrieve evidence from multiple meetings.
- Order evidence by meeting and timestamp.
- Detect statements that propose, confirm, change, or reject a decision.
- Use later explicit decisions to update the current state.
- Return the final decision and the important changes.
- Always attach meeting and timestamp evidence when available.
- If the evidence is unclear, say the decision is unresolved rather than inventing an answer.

## 8. Voice Agent Flow: Recommended Part 1
The team should select AssemblyAI's Voice Agent API, the managed option. The managed voice layer handles the real-time voice pipeline, while our application provides the custom meeting-memory tools.

```
Microphone
 ↓
AssemblyAI Voice Agent
 ↓
STT
 ↓
Tool Call: search_meeting_memory(question)
 ↓
RAG Retrieval
 ↓
Tool Call / Reasoning
 ↓
Final Decision Answer
 ↓
AssemblyAI TTS
 ↓
User hears the answer
```
This is preferable for the hackathon because the project's unique value is the memory + RAG + decision tracking, not rebuilding a voice pipeline from scratch.

## 9. Backend — Recommended Technology
| Technology / Library | Purpose | Priority |
|---|---|---|
| Python | Main backend language | Required |
| FastAPI | REST API and tool endpoints | Required |
| Uvicorn | FastAPI application server | Required |
| Pydantic | Shared request/response schemas | Required |
| PostgreSQL | Persistent storage for meetings, segments, and decisions | Required |
| SQLAlchemy | ORM / database models and queries | Required |
| Alembic | Database schema migrations | Required |
| psycopg2-binary | PostgreSQL driver | Required |
| AssemblyAI SDK/API | STT, diarization, and managed voice agent | Required |
| LLM SDK/API | Segmentation and decision reasoning | Required |
| sentence-transformers | Open-source embeddings | Recommended |
| NumPy | Vector calculations | Recommended |
| scikit-learn | Cosine similarity utilities | Recommended |
| python-dotenv | Environment variables/API keys | Recommended |
| pytest | Backend testing | Recommended |
| LangChain | LLM/tool abstraction if useful | Optional |
| LangGraph | More advanced agent workflow if needed | Optional |
| Ollama | Optional local LLM experimentation | Optional |

## 10. Open-Source RAG Approach
The retrieval part should remain simple and lightweight for the MVP.
```
Transcript Segment
 ↓
sentence-transformers
 ↓
Embedding Vector
 ↓
Persisted in PostgreSQL, loaded into memory at startup

User Question
 ↓
Question Embedding
 ↓
Cosine Similarity (in-memory)
 ↓
Top-K Segments
 ↓
LLM Reasoning
```
Recommended open-source libraries are sentence-transformers for embeddings and NumPy/scikit-learn for similarity calculations. Meetings, segments, and decisions are persisted in PostgreSQL so nothing is lost on restart; embeddings are loaded from PostgreSQL into an in-memory array at startup for fast cosine similarity — a dedicated vector database (FAISS, Chroma, Qdrant, or `pgvector` if you want similarity search inside Postgres itself) is unnecessary for 2–3 meetings but is a natural next step if the system grows.

## 11. Backend — Where to Start
1. Create the FastAPI project.
2. Create the shared Pydantic JSON schemas first.
3. Set up PostgreSQL, SQLAlchemy models, and the first Alembic migration.
4. Add the shared API key auth dependency and apply it to every route.
5. Prepare fake transcript JSON files for 2–3 meetings.
6. Build the segmentation module using mock LLM outputs.
7. Build embeddings and in-memory cosine-similarity retrieval, backed by PostgreSQL storage.
8. Build decision reasoning using retrieved segments.
9. Expose retrieval and reasoning as backend endpoints/tools.
10. Connect the real LLM.
11. Connect AssemblyAI for real transcription and diarization.
12. Connect the AssemblyAI Voice Agent.
13. Test the complete voice → retrieval → reasoning → speech flow.

## 12. Frontend — Recommended Technology
| Technology | Purpose | Priority |
|---|---|---|
| React + Vite | Main web application | Required |
| TypeScript | Type-safe frontend code and API models | Recommended |
| Tailwind CSS | Fast UI development | Recommended |
| HTML Audio API | Play audio and seek to timestamps | Required |
| WaveSurfer.js | Optional waveform/timeline visualization | Optional |
| Fetch or Axios | Backend communication | Required |

## 13. Frontend — Where to Start
1. Create the React + Vite project.
2. Build one main dashboard; avoid unnecessary pages.
3. Add a microphone/voice interaction area.
4. Add an AI answer section.
5. Add a decision timeline.
6. Show meeting, timestamp, speaker, and short summary.
7. Add an audio player.
8. Make every evidence item clickable.
9. On click, set the audio player's currentTime to the evidence timestamp.
10. Connect the UI to the FastAPI backend using the agreed JSON schemas.

## 14. Suggested Frontend Layout
```
-----------------------------------------------------------
| Conversation Memory Voice Agent |
| |
| 🎙 Ask by Voice |
| "What did we finally decide about the database?" |
| |
| AI Answer |
| The final decision was PostgreSQL... |
| |
| Decision Timeline |
| Meeting 1 | 08:20 | PostgreSQL proposed [▶] |
| Meeting 2 | 12:48 | Changed to MongoDB [▶] |
| Meeting 3 | 18:20 | Changed to PostgreSQL [▶] |
| |
| Audio: [===========●----------------] 18:20 |
-----------------------------------------------------------
```

## 15. Project Structure
Backend and frontend live as siblings under one project root, each self-contained, so deployment is just "point at the root and build both." Environment-specific values (API base URL, database URL, API keys) are read from `.env` files at each app's own root — nothing is hardcoded to a path — so moving or renaming the root doesn't break either app. PostgreSQL itself isn't part of this repo — `backend/.env` just points `DATABASE_URL` at whichever instance the team is using (a local install or a shared hosted database), and `alembic upgrade head` applies the schema to it.

```
project-root/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py              # PostgreSQL engine/session (SQLAlchemy)
│   │   ├── models/                  # SQLAlchemy ORM models (Postgres tables)
│   │   │   ├── __init__.py
│   │   │   ├── meeting.py
│   │   │   ├── segment.py
│   │   │   └── decision.py
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── meeting.py
│   │   │   ├── segment.py
│   │   │   ├── retrieval.py
│   │   │   └── decision.py
│   │   ├── modules/
│   │   │   ├── ingestion/
│   │   │   ├── segmentation/
│   │   │   ├── retrieval/
│   │   │   ├── reasoning/
│   │   │   └── voice/
│   │   ├── services/
│   │   │   ├── assemblyai.py
│   │   │   ├── embeddings.py
│   │   │   └── llm.py
│   │   ├── core/
│   │   │   └── security.py          # API key auth dependency, checked on every route
│   │   └── api/
│   │       ├── meetings.py
│   │       ├── search.py
│   │       └── voice.py
│   ├── alembic/                     # DB migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── data/
│   │   ├── audio/
│   │   └── transcripts/
│   ├── tests/
│   ├── .env                         # includes APP_API_KEY
│   ├── alembic.ini
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── VoiceInput.tsx
│   │   │   ├── AnswerCard.tsx
│   │   │   ├── DecisionTimeline.tsx
│   │   │   └── AudioPlayer.tsx
│   │   ├── hooks/
│   │   ├── api/
│   │   │   └── client.ts            # attaches Authorization header to every request
│   │   ├── types/
│   │   └── styles/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── .env                         # includes VITE_APP_API_KEY
│
├── .gitignore
└── README.md
```

## 16. Authentication
The MVP uses a **single shared API key**, not per-user accounts — consistent with keeping enterprise-style auth out of scope (§19). It's just enough to stop the demo API from being wide open on the public internet during the hackathon.

- A secret string is generated once and stored as `APP_API_KEY` in `backend/.env`.
- Every backend route except `GET /health` requires the header `Authorization: Bearer <APP_API_KEY>`, checked by a FastAPI dependency in `app/core/security.py`. A missing or wrong key returns `401 Unauthorized`.
- The frontend stores the same value as `VITE_APP_API_KEY` in `frontend/.env` and attaches it to every request in `src/api/client.ts`.
- The AssemblyAI Voice Agent's tool-calling configuration also sends this header when it invokes the backend's `/voice/tool/search_meeting_memory` endpoint.

**Known limitation, stated plainly rather than glossed over:** because the key ships inside the frontend's built JS bundle, anyone who opens browser dev tools can read it out of network requests. That's an acceptable trade for a hackathon demo behind a temporary URL, but it is not real security — if this ever needs to be a public-facing product, the API key must be replaced with real per-user authentication (e.g. JWT + login) before that happens.

## 17. Shared JSON Contracts
All modules should communicate using fixed JSON structures. This allows each team member to build and test their module without depending on another person's internal code. These same shapes are what get persisted as PostgreSQL rows (via the SQLAlchemy models in `backend/app/models/`), so the API contract and the database schema stay in sync.

**Transcript JSON**
```json
{
  "meeting_id": "meeting_2",
  "speaker": "Speaker A",
  "start_time": 748,
  "end_time": 775,
  "text": "Let's move from PostgreSQL to MongoDB."
}
```

**Decision Segment JSON**
```json
{
  "segment_id": "m2_s08",
  "meeting_id": "meeting_2",
  "start_time": 748,
  "end_time": 775,
  "topic": "Database",
  "summary": "The team decided to move to MongoDB.",
  "decision_text": "PostgreSQL -> MongoDB",
  "segment_text": "Let's move from PostgreSQL to MongoDB."
}
```

**Final Answer JSON**
```json
{
  "final_decision": "PostgreSQL",
  "answer": "The final decision was PostgreSQL.",
  "evidence": [
    {
      "meeting": "Meeting 2",
      "timestamp": "12:48",
      "change": "PostgreSQL -> MongoDB"
    },
    {
      "meeting": "Meeting 3",
      "timestamp": "18:20",
      "change": "MongoDB -> PostgreSQL"
    }
  ]
}
```

## 18. Module / Team Division
| Person | Module | Responsibility |
|---|---|---|
| Person A | Meeting Corpus + STT/Diarization | Create/record mock meetings, process audio with AssemblyAI, and output transcript JSON with speakers and timestamps. |
| Person B | Segmentation | Take transcript JSON → LLM → output topic/decision segments with timestamps and summaries. |
| Person C | Retrieval / RAG | Take segments → create embeddings → in-memory similarity search → return top-K relevant segments. |
| Person D | Decision Reasoning | Take retrieved segments → LLM reasoning → output final decision and exact evidence/change format. |
| Person E | Voice Agent Orchestration | Integrate AssemblyAI Voice Agent: mic input → STT → tool calls → TTS response. This is the glue layer. |
| Person F | Timeline UI + Audio | Take segment and decision JSON → render timeline → click item → jump to the correct audio timestamp. |

## 19. Example User Questions
| User Question | System Response |
|---|---|
| "What did we decide about the API redesign?" | Search all meetings, retrieve relevant API discussions, identify the final decision, and speak the answer. |
| "When did we change the database decision?" | Find the decision-change evidence and return the meeting and exact timestamp. |
| "How did our authentication decision evolve?" | Show the important decisions across meetings in chronological order. |
| "What did Speaker A say about deployment?" | Retrieve relevant speaker segments and provide the statement with its timestamp. |
| "Show me where we changed to MongoDB." | Return the relevant meeting/timestamp and let the user jump to that audio point. |

## 20. What the MVP Will NOT Try to Do
To keep the project feasible, the following are outside the initial scope:
- Thousands of meetings.
- Per-user accounts, login screens, roles, or permissions — a single shared API key covers the hackathon's needs (§16).
- A large-scale distributed vector database.
- Full video editing or video understanding.
- A general-purpose company knowledge platform.
- Building a custom real-time STT/TTS pipeline from scratch.
- Complicated multi-page frontend functionality.

## 21. Why the Project Is Feasible
The project is feasible because the MVP is intentionally controlled. The team only needs 2–3 scripted meetings, a small set of modules, and one clear end-to-end demonstration.
- The meeting dataset is small and controlled.
- Retrieval can run entirely in memory, backed by a single PostgreSQL instance for persistence.
- The modules have simple JSON interfaces.
- Each module can be developed and tested with fake data.
- AssemblyAI handles the difficult real-time voice layer.
- The frontend only needs one convincing dashboard.
- The final demo focuses on one strong use case: finding and explaining evolving decisions.

## 22. Weekly Development Plan
Hackathon window: **September 1 – September 30, 2026**. The whole team works in parallel every week — no one waits for a single person to finish their piece first. Fake/mock JSON data (defined in Week 1) is what makes this possible: every module can be built and tested against mock data before the real upstream module is ready, then swapped over once it is.

Every week ends with a **team sync + status update** (day/time to be fixed by the team) where each person reports: what shipped, what's blocked, what's next. Treat this as the checkpoint date for that week's Definition of Done row below.

| Week | Dates | All 6 roles work simultaneously on | Week-end Checkpoint |
|---|---|---|---|
| Week 1 | Sep 1 – Sep 7 | Team agrees & freezes shared JSON schemas + PostgreSQL table design + the `APP_API_KEY` auth approach (Day 1, blocking for everyone else). A: script + record mock meetings. B: segmentation module against mock transcripts. C: retrieval/embeddings skeleton against mock segments. D: decision-reasoning skeleton against mock segments. E: AssemblyAI Voice Agent sandbox test call. F: frontend dashboard scaffold against mock JSON. | Full pipeline runs end-to-end on 100% mock/fake data; PostgreSQL running with initial migration applied; every backend route rejects requests without the API key. |
| Week 2 | Sep 8 – Sep 14 | A: run real mock-meeting audio through AssemblyAI STT/diarization → real transcript JSON. B: connect real LLM to segmentation. C: real embeddings + similarity search on real segments, persisted to PostgreSQL. D: real decision reasoning tested against known decision-change scenarios. E: build tool-calling from Voice Agent to backend search endpoint. F: connect frontend to live backend endpoints instead of mock JSON. | Text-based Q&A works end-to-end over real transcribed meetings, reading from PostgreSQL. |
| Week 3 | Sep 15 – Sep 21 | E: wire up full voice loop (mic → STT → tool call → reasoning → TTS). F: build timeline UI with clickable evidence → audio seek. C/D: tune retrieval top-K and reasoning prompts against real test questions. A/B: expand/refine mock meeting scripts if retrieval quality is weak. | Full voice-in → voice-out flow works on at least one end-to-end question. |
| Week 4 | Sep 22 – Sep 28 | Whole team: bug fixes, edge cases, stub/fallback paths for any flaky external API, UI polish, write tests (backend + retrieval + seek). Record a backup demo video in case live demo fails. | Feature freeze — app is stable and demo-ready. |
| Week 5 | Sep 29 – Sep 30 | Whole team: rehearse the pitch, final run-through of the demo script, submission. | Submitted. |

## 23. Testing Requirements
- Test transcript-to-segment extraction using fixed sample transcripts.
- Test retrieval using questions with known correct answers.
- Check that top-K retrieval returns the expected meeting segments.
- Test decision reasoning using fixed retrieved evidence.
- Verify meeting IDs and timestamps are always valid.
- Verify that timeline clicks seek to the correct audio position.
- Test the complete voice flow from microphone to spoken answer.
- Test that requests without a valid `Authorization` header are rejected with `401` on every route except `/health`.
- Keep mock/stub endpoints available so one failed external integration does not stop the whole demo.

## 24. Definition of Done
- 2–3 mock meetings are available.
- Each meeting has transcript, speaker labels, and timestamps.
- Each transcript is divided into useful topic/decision segments.
- Segments have embeddings, persisted in PostgreSQL.
- Questions can retrieve relevant segments from multiple meetings.
- The LLM can identify a final decision and explain changes.
- Answers contain evidence with meeting and timestamp.
- Users can ask questions by voice.
- The system answers by voice.
- The UI displays the decision timeline.
- Clicking evidence jumps to the matching audio moment.
- Every backend route (except `/health`) enforces the shared API key.
- The application works end-to-end with a controlled demo dataset.

## 25. Final Recommended Stack
| Layer | Technology |
|---|---|
| Voice / STT / TTS / Turn-taking | AssemblyAI Voice Agent API — Part 1 Managed |
| Backend | Python + FastAPI + Uvicorn |
| Schemas | Pydantic |
| Database | PostgreSQL + SQLAlchemy + Alembic |
| Auth | Shared API key (`Authorization: Bearer <key>`) via FastAPI dependency |
| LLM | LLM API available/approved for the hackathon |
| Embeddings | sentence-transformers |
| Similarity Search | NumPy + scikit-learn cosine similarity (in-memory, loaded from PostgreSQL) |
| Frontend | React + Vite + TypeScript |
| UI Styling | Tailwind CSS |
| Audio | HTML Audio API |
| Optional Timeline | WaveSurfer.js |
| Testing | pytest + frontend testing tools |

## 26. Final Project Pitch
"Ask your team's past conversations anything by voice. The AI searches across multiple meetings, understands how decisions evolved, gives the final answer in speech, and takes you directly to the exact timestamp where the decision was discussed."

## 27. Final Implementation Recommendation
The safest development order is to build the core intelligence before connecting the real voice layer. Start with schemas, PostgreSQL models/migrations, and mock meeting JSON. Build segmentation, RAG retrieval, and decision reasoning. At the same time, the frontend can be developed using the same mock JSON. Once these pieces work, integrate AssemblyAI STT and diarization, then connect the managed Voice Agent, and finally connect the timeline to real audio.

This approach makes the project modular and feasible: even if an external API has a temporary issue, the core retrieval, reasoning, and UI can still be demonstrated with mock data.
