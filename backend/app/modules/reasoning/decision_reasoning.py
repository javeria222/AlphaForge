from typing import List, Dict, Any

from app.schemas.decision import DecisionResult, DecisionEvidence


class DecisionReasoner:
    """
    Deterministic decision reasoning engine.

    Takes conversation segments and extracts the latest
    explicit decision while preserving evidence.
    """

    def __init__(self):
        self.confirmation_keywords = [
            "agreed",
            "agree",
            "let's do",
            "let us do",
            "we'll use",
            "we will use",
            "decided",
            "decision is",
            "confirmed",
        ]

        self.rejection_keywords = [
            "reject",
            "rejected",
            "no",
            "don't",
            "do not",
            "not use",
            "cancel",
        ]

        self.change_keywords = [
            "change",
            "switch",
            "instead",
            "actually",
            "rather",
            "changed",
        ]

    def reason(self, segments: List[Dict[str, Any]]) -> DecisionResult:
        """
        Determine the latest decision from meeting segments.
        """

        if not segments:
            return DecisionResult(
                decision="No decision found",
                status="unresolved",
                evidence=[],
            )

        # Chronological order
        ordered_segments = sorted(
            segments,
            key=lambda segment: segment.get("timestamp", "")
        )

        decision = None
        status = "unresolved"
        evidence = []

        for segment in ordered_segments:
            text = segment.get("text", "").strip()

            if not text:
                continue

            lower_text = text.lower()

            # Explicit confirmation / decision
            if self._contains_keyword(
                lower_text,
                self.confirmation_keywords
            ):
                decision = self._extract_decision(text)
                status = "confirmed"

                evidence = [
                    self._create_evidence(segment)
                ]

            # Explicit change
            elif self._contains_keyword(
                lower_text,
                self.change_keywords
            ):
                decision = self._extract_decision(text)
                status = "confirmed"

                evidence = [
                    self._create_evidence(segment)
                ]

            # Explicit rejection
            elif self._contains_keyword(
                lower_text,
                self.rejection_keywords
            ):
                status = "rejected"

                evidence = [
                    self._create_evidence(segment)
                ]

        if decision is None:
            decision = "No clear decision found"

        return DecisionResult(
            decision=decision,
            status=status,
            evidence=evidence,
        )

    def _contains_keyword(
        self,
        text: str,
        keywords: List[str]
    ) -> bool:
        return any(keyword in text for keyword in keywords)

    def _extract_decision(self, text: str) -> str:
        """
        For the MVP, preserve the original statement as the decision.
        A later LLM layer can normalize this into a concise decision.
        """
        return text

    def _create_evidence(
        self,
        segment: Dict[str, Any]
    ) -> DecisionEvidence:

        return DecisionEvidence(
            meeting_id=str(
                segment.get("meeting_id", "unknown")
            ),
            timestamp=segment.get("timestamp"),
            speaker=segment.get("speaker"),
            text=segment.get("text", ""),
        )
