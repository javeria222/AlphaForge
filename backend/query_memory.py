import json
import os

def load_chunks(chunks_dir="data/chunks"):
    """
    Loads all structured meeting segments from the chunks directory.
    """
    all_segments = []
    if not os.path.exists(chunks_dir):
        return all_segments
        
    for filename in os.listdir(chunks_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(chunks_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_segments.extend(data)
    return all_segments

def semantic_search(query, top_k=2):
    """
    Simulates semantic search over structured meeting segments.
    (Can be replaced with real vector embeddings like OpenAI/SentenceTransformers later).
    """
    segments = load_chunks()
    if not segments:
        print("No chunks found. Run chunk_transcript.py first.")
        return []

    results = []
    query_lower = query.lower()
    
    for seg in segments:

        score = 0
        if query_lower in seg.get("topic", "").lower():
            score += 2
        if query_lower in seg.get("summary", "").lower():
            score += 1
            
        if score > 0:
            results.append((score, seg))
            
    results.sort(key=lambda x: x[0], reverse=True)
    return [res[1] for res in results[:top_k]]

if __name__ == "__main__":
    query = "semantic architecture"
    print(f"Searching memory for: '{query}'")
    matches = semantic_search(query)
    
    for match in matches:
        print(f"\n[Found Segment: {match.get('segment_id')}]")
        print(f"Topic: {match.get('topic')}")
        print(f"Summary: {match.get('summary')}")
        print(f"Decision: {match.get('decision_text')}")