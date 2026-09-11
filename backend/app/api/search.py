from fastapi import APIRouter, Depends
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.retrieval import RetrievalQuery, RetrievalOutput, RetrievalResult
from app.schemas.answer import AnswerQuery, FinalAnswerOutput
from app.core.security import verify_api_key, ErrorResponse
from app.services.embeddings import embeddings_service
from app.services.mock_data import get_mock_segments

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
    segments = get_mock_segments()
    query_vec = embeddings_service.encode(query.query)

    scored = []
    for seg in segments:
        sim = cosine_similarity([query_vec], [seg["embedding"]])[0][0]
        if seg["decision_text"] is not None:
            sim = min(sim + 0.1, 1.0)
        scored.append((seg, round(float(sim), 2)))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    top_results = scored[: query.top_k]

    results = [
        RetrievalResult(
            segment_id=seg["segment_id"],
            meeting_id=seg["meeting_id"],
            score=score,
            start_time=seg["start_time"],
            end_time=seg["end_time"],
            topic=seg["topic"],
            summary=seg["summary"],
            decision_text=seg["decision_text"],
            segment_text=seg["segment_text"],
        )
        for seg, score in top_results
    ]

    return RetrievalOutput(query=query.query, top_k=query.top_k, results=results)


@router.post(
    "/answer",
    response_model=FinalAnswerOutput,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}}
)
async def answer_question(query: AnswerQuery, db: Session = Depends(get_db)):
    """
    Run retrieval + reasoning internally to answer a question.
    Body: { "question": string }
    Returns a Final Answer Output.
    This is the main endpoint the app is built around.
    Owner: Person D (Contract §3)
    """
    # TODO(PersonD): Implement decision reasoning
    # This should internally call retrieval and reasoning
    pass

