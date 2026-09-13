from unittest.mock import MagicMock, patch

import numpy as np

from app.models.segment import Segment
from app.modules.retrieval.retriever import retrieve_segments


def make_segment(segment_id, embedding, decision_text=None, meeting_id="meeting_1"):
    return Segment(
        segment_id=segment_id,
        meeting_id=meeting_id,
        start_time=0,
        end_time=10,
        speaker="Speaker A",
        topic="Database",
        summary="summary",
        decision_text=decision_text,
        segment_text="segment text",
        embedding=embedding,
    )


def make_db(segments):
    db = MagicMock()
    db.query.return_value.all.return_value = segments
    return db


def test_decision_boost_changes_ranking():
    # Without the boost, no_decision (0.65) would outrank decision (0.60).
    # With the +0.1 boost, decision (0.70) should come out ahead.
    decision_seg = make_segment("s1", [0.6, 0.8], decision_text="Use MongoDB")
    no_decision_seg = make_segment("s2", [0.65, 0.7599])

    db = make_db([decision_seg, no_decision_seg])

    with patch("app.modules.retrieval.retriever.embeddings_service") as mock_emb:
        mock_emb.encode.return_value = np.array([1, 0])
        results = retrieve_segments("test query", top_k=5, db=db)

    assert results[0].segment_id == "s1"
    assert results[0].score == 0.7
    assert results[1].segment_id == "s2"
    assert results[1].score == 0.65


def test_score_floors_at_zero_not_negative():
    opposite_seg = make_segment("s1", [-1, 0])
    db = make_db([opposite_seg])

    with patch("app.modules.retrieval.retriever.embeddings_service") as mock_emb:
        mock_emb.encode.return_value = np.array([1, 0])
        results = retrieve_segments("test query", top_k=5, db=db)

    assert results[0].score == 0.0


def test_score_caps_at_one_after_boost():
    perfect_match = make_segment("s1", [1, 0], decision_text="Confirmed")
    db = make_db([perfect_match])

    with patch("app.modules.retrieval.retriever.embeddings_service") as mock_emb:
        mock_emb.encode.return_value = np.array([1, 0])
        results = retrieve_segments("test query", top_k=5, db=db)

    assert results[0].score == 1.0


def test_top_k_limits_results():
    segments = [make_segment(f"s{i}", [1, 0]) for i in range(5)]
    db = make_db(segments)

    with patch("app.modules.retrieval.retriever.embeddings_service") as mock_emb:
        mock_emb.encode.return_value = np.array([1, 0])
        results = retrieve_segments("test query", top_k=2, db=db)

    assert len(results) == 2


def test_empty_database_returns_empty_list():
    db = make_db([])

    with patch("app.modules.retrieval.retriever.embeddings_service") as mock_emb:
        mock_emb.encode.return_value = np.array([1, 0])
        results = retrieve_segments("test query", top_k=5, db=db)

    assert results == []


def test_skips_segments_with_no_embedding():
    good_seg = make_segment("s1", [1, 0])
    broken_seg = make_segment("s2", None)
    db = make_db([good_seg, broken_seg])

    with patch("app.modules.retrieval.retriever.embeddings_service") as mock_emb:
        mock_emb.encode.return_value = np.array([1, 0])
        results = retrieve_segments("test query", top_k=5, db=db)

    assert len(results) == 1
    assert results[0].segment_id == "s1"