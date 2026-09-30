from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):

        print("Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully!")

    def get_embedding(self, text: str) -> list[float]:

        embedding = self.model.encode(text)
        return embedding.tolist()

    @staticmethod
    def calculate_similarity(vec1: list[float], vec2: list[float]) -> float:

        v1 = np.array(vec1)
        v2 = np.array(vec2)


        cosine_similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return float(cosine_similarity)



embedding_service = EmbeddingService()