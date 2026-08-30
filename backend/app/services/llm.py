"""LLM service for reasoning and decision extraction"""

class LLMService:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def extract_decisions(self, text: str) -> list:
        """Extract decisions from meeting transcript"""
        pass
    
    async def generate_answer(self, question: str, context: str) -> str:
        """Generate answer based on context"""
        pass
