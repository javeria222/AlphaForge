from app.modules.reasoning.decision_reasoning import DecisionReasoner


def test_confirmed_decision():
    segments = [
        {
            "meeting_id": "meeting_1",
            "timestamp": "10:00",
            "speaker": "Alice",
            "text": "I propose we use PostgreSQL.",
        },
        {
            "meeting_id": "meeting_1",
            "timestamp": "10:05",
            "speaker": "Bob",
            "text": "Agreed, let's use PostgreSQL.",
        },
    ]

    reasoner = DecisionReasoner()
    result = reasoner.reason(segments)

    assert result.status == "confirmed"
    assert "PostgreSQL" in result.decision
    assert len(result.evidence) == 1


def test_no_decision():
    segments = [
        {
            "meeting_id": "meeting_1",
            "timestamp": "10:00",
            "speaker": "Alice",
            "text": "We could use PostgreSQL.",
        }
    ]

    reasoner = DecisionReasoner()
    result = reasoner.reason(segments)

    assert result.status == "unresolved"


def test_later_change_overrides_previous_decision():
    segments = [
        {
            "meeting_id": "meeting_1",
            "timestamp": "10:00",
            "speaker": "Alice",
            "text": "Agreed, let's use PostgreSQL.",
        },
        {
            "meeting_id": "meeting_2",
            "timestamp": "10:10",
            "speaker": "Alice",
            "text": "Actually, let's switch to MongoDB.",
        },
    ]

    result = DecisionReasoner().reason(segments)

    assert result.status == "confirmed"
    assert "MongoDB" in result.decision
    assert result.evidence[0].meeting_id == "meeting_2"


def test_evidence_is_preserved():
    segments = [
        {
            "meeting_id": "meeting_3",
            "timestamp": "14:32",
            "speaker": "Speaker D",
            "text": "The final decision is to postpone the launch.",
        }
    ]

    result = DecisionReasoner().reason(segments)

    assert result.status == "confirmed"
    assert result.evidence[0].meeting_id == "meeting_3"
    assert result.evidence[0].timestamp == "14:32"
    assert result.evidence[0].speaker == "Speaker D"
    assert result.evidence[0].text == (
        "The final decision is to postpone the launch."
    )