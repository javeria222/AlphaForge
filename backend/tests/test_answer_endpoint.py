from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import search
from app.core.security import verify_api_key
from app.database import get_db


def r(segment_id, meeting_id, start, topic, decision, score):
    return SimpleNamespace(
        segment_id=segment_id, meeting_id=meeting_id, start_time=start, end_time=start + 5,
        topic=topic, summary="s", decision_text=decision, segment_text="t", score=score,
    )


class FakeDB:
    def query(self, _model):
        meetings = [
            SimpleNamespace(meeting_id="meeting_1", title="Kickoff - Architecture Planning", date="2026-09-01"),
            SimpleNamespace(meeting_id="meeting_2", title="Backend Sync - Database Discussion", date="2026-09-08"),
            SimpleNamespace(meeting_id="meeting_3", title="Final Review", date="2026-09-15"),
        ]
        return SimpleNamespace(all=lambda: meetings)


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(search.router, prefix="/api")
    app.dependency_overrides[verify_api_key] = lambda: None
    app.dependency_overrides[get_db] = lambda: FakeDB()
    return TestClient(app)


def test_answer_builds_three_row_timeline(client, monkeypatch):
    monkeypatch.setattr(search, "retrieve_segments", lambda q, k, db: [
        r("m3_s04", "meeting_3", 5, "Database", "MongoDB -> PostgreSQL", 0.81),
        r("m2_s03", "meeting_2", 9, "Database", "PostgreSQL -> MongoDB", 0.79),
        r("m1_s03", "meeting_1", 40, "Database", "Proposed PostgreSQL", 0.74),
        r("m1_s05", "meeting_1", 62, "Deployment", "Deploy via Docker", 0.40),
        r("m2_s02", "meeting_2", 4, "Database", None, 0.90),
    ])
    body = client.post("/api/answer", json={"question": "What did we decide about the database?"}).json()

    assert body["status"] == "resolved"
    assert body["final_decision"] == "PostgreSQL"
    assert [e["segment_id"] for e in body["evidence"]] == ["m1_s03", "m2_s03", "m3_s04"]
    assert body["evidence"][0]["meeting_title"] == "Kickoff - Architecture Planning"
    assert body["evidence"][0]["timestamp"] == "00:40"
    assert "went back from MongoDB to PostgreSQL" in body["answer"]


def test_unrelated_question_is_unresolved(client, monkeypatch):
    monkeypatch.setattr(search, "retrieve_segments", lambda q, k, db: [
        r("m1_s03", "meeting_1", 40, "Database", "Proposed PostgreSQL", 0.08),
    ])
    body = client.post("/api/answer", json={"question": "What is the weather?"}).json()
    assert body["status"] == "unresolved" and body["final_decision"] is None and body["evidence"] == []


def test_retrieval_failure_is_502(client, monkeypatch):
    def boom(q, k, db):
        raise RuntimeError("db down")
    monkeypatch.setattr(search, "retrieve_segments", boom)
    resp = client.post("/api/answer", json={"question": "x"})
    assert resp.status_code == 502
    assert resp.json()["detail"]["code"] == "UPSTREAM_ERROR"