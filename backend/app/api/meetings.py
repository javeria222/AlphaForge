from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.meeting import Meeting, MeetingCreate, MeetingListResponse
from app.schemas.segment import SegmentListResponse
from app.schemas.transcript import TranscriptOutput
from app.models.meeting import Meeting as MeetingModel, MeetingStatus
from app.models.segment import Segment as SegmentModel
from app.core.security import verify_api_key, ErrorResponse
from pydantic import BaseModel

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post(
    "/",
    response_model=Meeting,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}}
)
async def create_meeting(meeting: MeetingCreate, db: Session = Depends(get_db)):
    """
    Upload a new meeting (audio file + title).
    Returns a Meeting with status: 'uploaded'.
    Owner: Person A (Contract §3)
    """
    # TODO(PersonA): Implement meeting creation logic
    pass


@router.get(
    "/",
    response_model=MeetingListResponse,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}}
)
async def list_meetings(db: Session = Depends(get_db)):
    """
    List all meetings.
    Returns { "meetings": [Meeting, ...] }
    Owner: Person A/F (Contract §3)
    """
    # TODO(PersonA): Implement meeting listing logic
    pass


@router.get(
    "/{meeting_id}",
    response_model=Meeting,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def get_meeting(meeting_id: str, request: Request, db: Session = Depends(get_db)):
    meeting = db.query(MeetingModel).filter(MeetingModel.meeting_id == meeting_id).first()
    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "code": "NOT_FOUND", "message": f"Meeting '{meeting_id}' not found"},
        )

    # The frontend plays audio_url directly, so a relative path must become an
    # absolute URL pointing at this backend, not at the Vite dev server.
    audio_url = meeting.audio_url
    if audio_url.startswith("/"):
        audio_url = str(request.base_url).rstrip("/") + audio_url

    return Meeting(
        meeting_id=meeting.meeting_id, title=meeting.title, date=meeting.date,
        audio_url=audio_url, duration_seconds=meeting.duration_seconds,
        status=meeting.status,
    )


@router.get(
    "/{meeting_id}/transcript",
    response_model=TranscriptOutput,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}}
)
async def get_transcript(meeting_id: str, db: Session = Depends(get_db)):
    """
    Get the raw transcript for one meeting.
    Returns a Transcript Output.
    404 if not yet transcribed.
    409 (NOT_READY) if transcription is in progress.
    Owner: Person A/B (Contract §3)
    """
    # TODO(PersonA): Implement transcript retrieval
    pass


@router.get(
    "/{meeting_id}/segments",
    response_model=SegmentListResponse,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}}
)
async def get_segments(meeting_id: str, db: Session = Depends(get_db)):
    """
    Get decision segments for one meeting.
    Returns { "meeting_id": ..., "segments": [...] }
    Owner: Person B/C (Contract §3)
    """
    meeting = db.query(MeetingModel).filter(MeetingModel.meeting_id == meeting_id).first()
    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "code": "NOT_FOUND", "message": f"Meeting '{meeting_id}' not found"},
        )
    
    if meeting.status != MeetingStatus.ready: 
            raise HTTPException(
                status_code=409, 
                detail={"error": True, "code": "NOT_READY", "message": f"Meeting '{meeting_id}' is not ready yet (status: {meeting.status.value})"}
            )

    segments = db.query(SegmentModel).filter(SegmentModel.meeting_id == meeting_id).all()
    return SegmentListResponse(meeting_id=meeting_id, segments=segments)



