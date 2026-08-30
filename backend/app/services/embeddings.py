"""Embeddings service for semantic search"""

class EmbeddingsService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
    
    def encode(self, text: str):
        """Generate embedding for text"""
        pass
