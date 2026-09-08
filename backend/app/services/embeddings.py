from sentence_transformers import SentenceTransformer

class EmbeddingsService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def encode(self, text: str):
        return self.model.encode(text)


embeddings_service = EmbeddingsService()