import json
import os
import sys

def search_meeting_memory(query: str, chunks_json_path: str = "data/chunks/meeting_1.json"):
    print(f"Loading chunks from {chunks_json_path}...")
    
    if not os.path.exists(chunks_json_path):
        print(f"Error: Chunks file not found at {chunks_json_path}")
        return
        
    with open(chunks_json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    print(f"\nSearching across {len(chunks)} meeting chunks for: '{query}'\n" + "="*50)
    
    matches = []
    query_lower = query.lower()
    
    for idx, chunk in enumerate(chunks):
        if query_lower in chunk["text"].lower():
            matches.append((idx + 1, chunk))
            
    if not matches:
        print("No direct keyword matches found in the chunks. Try a broader search term.")
        return
        
    print(f"Found {len(matches)} relevant segment(s):\n")
    for chunk_num, chunk in matches:
        speakers_str = ", ".join(chunk.get("speakers", []))
        print(f"[Chunk #{chunk_num}] (Speakers: {speakers_str})")
        print(f"Snippet: {chunk['text'].strip()}")
        print("-" * 50)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        search_query = " ".join(sys.argv[1:])
    else:
        search_query = "data" 
        
    search_meeting_memory(search_query)