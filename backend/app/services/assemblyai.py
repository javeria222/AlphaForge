"""AssemblyAI service for audio transcription"""

class AssemblyAIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def transcribe_audio(self, audio_file: str) -> str:
        """Transcribe audio file using AssemblyAI API"""
        pass
