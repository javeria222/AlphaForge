from fastapi import APIRouter, HTTPException, UploadFile, File
from app.modules.voice.agent import voice_agent

router = APIRouter(prefix="/voice", tags=["Voice Agent"])

@router.post("/process-audio")
async def process_audio_endpoint(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        response = await voice_agent.handle_audio_stream(audio_bytes)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query-text")
async def query_text_endpoint(query: str):

    answer = await voice_agent.process_text_query(query)
    return {"query": query, "response": answer}