from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from pydantic import BaseModel

security = HTTPBearer(auto_error=False)


class ErrorResponse(BaseModel):
    """Standard error response per contract §1."""
    error: bool = True
    code: str
    message: str


async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify API key on protected routes per contract §1.5.
    Expects: Authorization: Bearer <APP_API_KEY>
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "code": "UNAUTHORIZED", "message": "Missing or invalid API key."}
        )

    if credentials.credentials != settings.APP_API_KEY:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "code": "UNAUTHORIZED", "message": "Missing or invalid API key."}
        )

    return credentials.credentials

