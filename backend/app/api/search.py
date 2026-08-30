from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.retrieval import RetrievalQuery, RetrievalOutput
from app.schemas.answer import AnswerQuery, FinalAnswerOutput
from app.core.security import verify_api_key, ErrorResponse

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
    Body: { "query": string, "top_k"?: int (default 5) }
    Returns a Retrieval Output.
    Owner: Person C (Contract §3)
    """
    # TODO(PersonC): Implement retrieval/similarity search
    pass


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

