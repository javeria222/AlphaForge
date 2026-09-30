"""Turn retrieved, hand-labeled decision segments into a decision timeline + spoken answer.

Deterministic on purpose: the seed labels `decision_text` as "A -> B", "Proposed X"
or "Deploy via X", so no keyword guessing or LLM call is needed.
"""
from typing import Optional

# Ignore decision segments that barely match the question, so an unrelated
# question ("what's the weather?") ends up "unresolved" instead of answering
# with some database decision. Tune this against real queries.
MIN_SCORE = 0.25

_PREFIXES = ("proposed ", "deploy via ", "use ")


def parse_change(decision_text: str) -> tuple[Optional[str], str]:
    """Return (from_value, to_value). from_value is None for a first choice."""
    text = decision_text.strip()
    for arrow in ("->", "→"):
        if arrow in text:
            left, right = text.split(arrow, 1)
            return (left.strip() or None), right.strip()
    for prefix in _PREFIXES:
        if text.lower().startswith(prefix):
            return None, text[len(prefix):].strip()
    return None, text


def select_decisions(results, min_score: float = MIN_SCORE):
    """Keep the decision segments that belong to the best-matching topic."""
    decisions = [r for r in results if r.decision_text and r.score >= min_score]
    if not decisions:
        return []
    anchor = max(decisions, key=lambda r: r.score)
    return [r for r in decisions if r.topic == anchor.topic]


def chronological(results, dates: dict):
    """Meeting date first, then position inside the meeting."""
    return sorted(results, key=lambda r: (dates.get(r.meeting_id, ""), r.meeting_id, r.start_time))


def narrate(steps: list[dict]) -> str:
    """steps: [{'title': str, 'change': str}, ...] in chronological order. Speakable, no markdown."""
    if not steps:
        return "I could not find a clear decision in the meetings."

    final = parse_change(steps[-1]["change"])[1]
    parts = [f"The final decision is {final}."]
    seen: set[str] = set()

    for step in steps:
        frm, to = parse_change(step["change"])
        title = step["title"]
        if frm is None:
            parts.append(f"In {title}, the team chose {to}.")
        elif to.lower() in seen:
            parts.append(f"In {title}, they went back from {frm} to {to}.")
        else:
            parts.append(f"In {title}, they switched from {frm} to {to}.")
        if frm:
            seen.add(frm.lower())
        seen.add(to.lower())

    return " ".join(parts)