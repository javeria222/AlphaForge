from types import SimpleNamespace

from app.modules.reasoning.timeline import chronological, narrate, parse_change, select_decisions


def seg(segment_id, meeting_id, start, topic, decision, score):
    return SimpleNamespace(
        segment_id=segment_id, meeting_id=meeting_id, start_time=start,
        topic=topic, decision_text=decision, score=score,
    )


def test_parse_change():
    assert parse_change("PostgreSQL -> MongoDB") == ("PostgreSQL", "MongoDB")
    assert parse_change("Proposed PostgreSQL") == (None, "PostgreSQL")
    assert parse_change("Deploy via Docker") == (None, "Docker")
    assert parse_change("Ship it") == (None, "Ship it")


def test_select_keeps_best_topic_only():
    results = [
        seg("m1_s03", "meeting_1", 12, "Database", "Proposed PostgreSQL", 0.7),
        seg("m1_s05", "meeting_1", 30, "Deployment", "Deploy via Docker", 0.4),
        seg("m2_s03", "meeting_2", 9, "Database", "PostgreSQL -> MongoDB", 0.8),
        seg("m2_s02", "meeting_2", 4, "Database", None, 0.9),  # discussion: never evidence
    ]
    picked = select_decisions(results)
    assert {r.segment_id for r in picked} == {"m1_s03", "m2_s03"}


def test_low_scores_are_ignored():
    assert select_decisions([seg("a", "meeting_1", 1, "Database", "Proposed X", 0.1)]) == []


def test_order_is_by_meeting_date_not_raw_start_time():
    # meeting_3's decision starts EARLIER in its own audio than meeting_1's.
    results = [
        seg("m3_s04", "meeting_3", 5, "Database", "MongoDB -> PostgreSQL", 0.8),
        seg("m1_s03", "meeting_1", 40, "Database", "Proposed PostgreSQL", 0.7),
    ]
    dates = {"meeting_1": "2026-09-01", "meeting_3": "2026-09-15"}
    assert [r.segment_id for r in chronological(results, dates)] == ["m1_s03", "m3_s04"]


def test_narrative_goes_back_to_postgres():
    text = narrate([
        {"title": "Kickoff", "change": "Proposed PostgreSQL"},
        {"title": "Backend Sync", "change": "PostgreSQL -> MongoDB"},
        {"title": "Final Review", "change": "MongoDB -> PostgreSQL"},
    ])
    assert text.startswith("The final decision is PostgreSQL.")
    assert "In Kickoff, the team chose PostgreSQL." in text
    assert "In Backend Sync, they switched from PostgreSQL to MongoDB." in text
    assert "In Final Review, they went back from MongoDB to PostgreSQL." in text
    assert "->" not in text and "*" not in text