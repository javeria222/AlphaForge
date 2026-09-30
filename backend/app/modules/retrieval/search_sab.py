from typing import List, Dict, Any

class ContextRetrieval:
    def __init__(self):
        pass

    def find_relevant_context(self, query: str, stored_embeddings: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:


        sorted_contexts = sorted(stored_embeddings, key=lambda x: x.get("score", 0.0), reverse=True)
        return sorted_contexts[:top_k]