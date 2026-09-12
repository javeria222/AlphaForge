from fastapi import APIRouter, Depends
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.retrieval import RetrievalQuery, RetrievalOutput
from app.schemas.answer import AnswerQuery, FinalAnswerOutput
from app.core.security import verify_api_key, ErrorResponse
from app.services.embeddings import embeddings_service
from app.services.mock_data import get_mock_segments
from app.schemas.answer import AnswerQuery, FinalAnswerOutput, Evidence
from app.modules.retrieval.retriever import retrieve_segments
router = APIRouter(tags=["search"])


@router.post(
    "/search",
    response_model=RetrievalOutput,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}}
)
async def search_segments(query: RetrievalQuery, db: Session = Depends(get_db)):
    """
    Search across all meetings for relevant segments via semantic similarity.
    Owner: Person C (Contract §3)
    """
    results = retrieve_segments(query.query, query.top_k, db)
    return RetrievalOutput(query=query.query, top_k=query.top_k, results=results)


@router.post(
    "/answer",
    response_model=FinalAnswerOutput,
    dependencies=[Depends(verify_api_key)],
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
    },
)
async def answer_question(
    query: AnswerQuery,
    db: Session = Depends(get_db),
):
    """
    Run retrieval + reasoning internally to answer a question.

    Body: { "question": string }
    Returns a Final Answer Output.

    Owner: Person D (Contract §3)
    """

    from app.modules.reasoning.decision_reasoning import DecisionReasoner

    # 1. Retrieve meeting segments
    segments = get_mock_segments()

    query_vec = embeddings_service.encode(query.question)

    scored = []

    for seg in segments:
        sim = cosine_similarity(
            [query_vec],
            [seg["embedding"]],
        )[0][0]

        # Person C's +0.1 decision boost
        if seg["decision_text"] is not None:
            sim = min(sim + 0.1, 1.0)

        scored.append((seg, float(sim)))

    scored.sort(key=lambda pair: pair[1], reverse=True)

    # Use the most relevant segments for reasoning
    top_segments = [seg for seg, _ in scored[:5]]

    # 2. Convert retrieved segments to reasoning input
    reasoning_segments = [
        {
            "meeting_id": seg["meeting_id"],
            "timestamp": str(seg["start_time"]),
            "speaker": seg.get("speaker", "Unknown"),
            "text": seg.get("decision_text") or seg["segment_text"],
        }
        for seg in top_segments
    ]

    # 3. Run Person D decision reasoning
    result = DecisionReasoner().reason(reasoning_segments)

    # 4. Convert evidence into the API response format
    evidence = []

    for reasoning_evidence in result.evidence:
        matching_segment = next(
            (
                seg
                for seg in top_segments
                if str(seg["meeting_id"]) == reasoning_evidence.meeting_id
                and (
                    seg.get("decision_text") == reasoning_evidence.text
                    or seg["segment_text"] == reasoning_evidence.text
                )
            ),
            None,
        )

        if matching_segment is None:
            continue

        start_time = int(matching_segment["start_time"])

        minutes = start_time // 60
        seconds = start_time % 60

        evidence.append(
            Evidence(
                segment_id=matching_segment["segment_id"],
                meeting_id=matching_segment["meeting_id"],
                meeting_title=matching_segment.get(
                    "meeting_title",
                    "Unknown Meeting",
                ),
                start_time=start_time,
                timestamp=f"{minutes:02d}:{seconds:02d}",
                change=reasoning_evidence.text,
            )
        )

    # Contract: evidence is chronological
    evidence.sort(key=lambda item: item.start_time)

    # 5. Build final speakable response
    if result.status == "confirmed":
        status = "resolved"
        final_decision = result.decision
        answer = f"The decision was: {result.decision}"
    else:
        status = "unresolved"
        final_decision = None
        answer = "I could not find a clear decision in the meeting."

    return FinalAnswerOutput(
        question=query.question,
        status=status,
        final_decision=final_decision,
        answer=answer,
        evidence=evidence,
    )