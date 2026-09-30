from typing import List

class TranscriptChunker:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def chunk_text(self, text: str) -> List[str]:
        """
        تقسيم النصوص الطويلة إلى أجزاء صغيرة (Chunks) لسهولة البحث والتضمين (Embeddings).
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)
        return chunks