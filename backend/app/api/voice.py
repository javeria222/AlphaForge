from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.answer import AnswerQuery, FinalAnswerOutput
from app.core.security import verify_api_key, ErrorResponse

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post(
    "/tool/search_meeting_memory",
    response_model=FinalAnswerOutput,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}}
)
async def voice_search_meeting_memory(query: AnswerQuery, db: Session = Depends(get_db)):
    """
    Tool-call endpoint the AssemblyAI Voice Agent invokes mid-conversation.
    Same request/response shape as /answer.
    Kept as a separate route for voice-specific logging/latency handling.
    
    The Voice Agent's tool-calling config must send the Authorization header on this call.
    
    Tool schema (Contract §3.1):
    {
      "name": "search_meeting_memory",
      "description": "Search across all past meetings to answer a question about a decision, topic, or discussion.",
      "input_schema": {
        "type": "object",
        "properties": {
          "question": {
            "type": "string",
            "description": "The user's question, in natural language, exactly as asked."
          }
        },
        "required": ["question"]
      }
    }
    
    Owner: Person E (Contract §3)
    """
    # TODO(PersonE): Implement voice agent tool orchestration
    # This should have the same business logic as /answer but with voice-specific handling
    pass

