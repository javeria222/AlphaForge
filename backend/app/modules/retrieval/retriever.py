from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.models.segment import Segment
from app.schemas.retrieval import RetrievalResult
from app.services.embeddings import embeddings_service


def retrieve_segments(query: str, top_k: int, db: Session) -> list[RetrievalResult]:
    """
    Rank all segments in the database against the query string via cosine similarity.
    Owner: Person C (Contract §3)
    """
    segments = db.query(Segment).all()

    if not segments:
        return []

    query_vec = embeddings_service.encode(query)

    scored = []
    for seg in segments:
        if seg.embedding is None:
            continue
        sim = cosine_similarity([query_vec], [seg.embedding])[0][0]
        sim = max(0.0, float(sim))  # floor per contract
        if seg.decision_text is not None:
            sim = min(sim + 0.1, 1.0)  # boost, capped per contract
        scored.append((seg, round(sim, 2)))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    top_results = scored[:top_k]

    return [
        RetrievalResult(
            segment_id=seg.segment_id,
            meeting_id=seg.meeting_id,
            score=score,
            start_time=seg.start_time,
            end_time=seg.end_time,
            topic=seg.topic,
            summary=seg.summary,
            decision_text=seg.decision_text,
            segment_text=seg.segment_text,
        )
        for seg, score in top_results
    ]