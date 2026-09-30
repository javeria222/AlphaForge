from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import ErrorResponse, verify_api_key
from app.database import get_db
from app.models.meeting import Meeting as MeetingModel
from app.modules.reasoning.timeline import chronological, narrate, parse_change, select_decisions
from app.modules.retrieval.retriever import retrieve_segments
from app.schemas.answer import AnswerQuery, Evidence, FinalAnswerOutput
from app.schemas.retrieval import RetrievalOutput, RetrievalQuery

ANSWER_TOP_K = 10


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
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
)
async def answer_question(query: AnswerQuery, db: Session = Depends(get_db)):
    try:
        results = retrieve_segments(query.question, ANSWER_TOP_K, db)
        meetings = {m.meeting_id: m for m in db.query(MeetingModel).all()}
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail={"error": True, "code": "UPSTREAM_ERROR", "message": f"Retrieval failed: {exc}"},
        )

    dates = {mid: m.date for mid, m in meetings.items()}
    decisions = chronological(select_decisions(results), dates)

    if not decisions:
        return FinalAnswerOutput(
            question=query.question, status="unresolved", final_decision=None,
            answer="I could not find a clear decision about that in the meetings.", evidence=[],
        )

    evidence, steps = [], []
    for seg in decisions:
        meeting = meetings.get(seg.meeting_id)
        title = meeting.title if meeting else "Unknown Meeting"
        evidence.append(Evidence(
            segment_id=seg.segment_id, meeting_id=seg.meeting_id, meeting_title=title,
            start_time=seg.start_time,
            timestamp=f"{seg.start_time // 60:02d}:{seg.start_time % 60:02d}",
            change=seg.decision_text,
        ))
        steps.append({"title": title, "change": seg.decision_text})

    return FinalAnswerOutput(
        question=query.question, status="resolved",
        final_decision=parse_change(decisions[-1].decision_text)[1],
        answer=narrate(steps), evidence=evidence,
    )