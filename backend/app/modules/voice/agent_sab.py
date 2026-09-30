from typing import List, Dict, Any
from app.services.llm import LLMService

class VoiceAgentOrchestrator:
    def __init__(self):
        self.llm_service = LLMService()

    async def handle_audio_stream(self, audio_bytes: bytes) -> str:
        """
        معالجة تدفق الصوت الوارد (Audio Stream) وتحويله أو تحليله.
        """
        # محاكاة معالجة الصوت
        return "Audio processed successfully by Voice Agent."

    async def process_text_query(self, query: str) -> str:
        """
        معالجة استعلام النص المباشر عبر الـ LLM.
        """
        prompt = f"User Query: {query}"
        response = self.llm_service.generate(prompt)
        return response

# إنشاء نسخة جاهزة للاستيراد في الروتر
voice_agent = VoiceAgentOrchestrator()