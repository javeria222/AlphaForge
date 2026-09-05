import json
import os

def chunk_transcript(json_path: str, max_chunk_words: int = 500):
    print(f"Loading transcript from {json_path}...")
    
    if not os.path.exists(json_path):
        print(f"Error: Transcript not found at {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        segments = json.load(f)
        
    chunks = []
    current_chunk = {
        "speakers": set(),
        "start_time": segments[0]["start_time"] if segments else 0,
        "end_time": 0,
        "text": ""
    }
    
    current_word_count = 0
    
    for seg in segments:
        words = seg["text"].split()
        word_count = len(words)
        
        current_chunk["speakers"].add(seg["speaker"])
        current_chunk["end_time"] = seg["end_time"]
        current_chunk["text"] += " " + seg["text"]
        current_word_count += word_count
        
        # Agar ek chunk ka size limit cross kar jaye toh naya chunk shuru karein
        if current_word_count >= max_chunk_words:
            current_chunk["speakers"] = list(current_chunk["speakers"])
            chunks.append(current_chunk)
            
            # Reset for next chunk
            current_chunk = {
                "speakers": set(),
                "start_time": seg["start_time"],
                "end_time": seg["end_time"],
                "text": ""
            }
            current_word_count = 0
            
    # Add the remaining text as the final chunk
    if current_word_count > 0:
        current_chunk["speakers"] = list(current_chunk["speakers"])
        chunks.append(current_chunk)
        
    # Save chunks to a new JSON file
    output_path = json_path.replace("transcripts", "chunks")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)
        
    print(f"Success! Created {len(chunks)} chunks. Saved to: {output_path}")

if __name__ == "__main__":
    TRANSCRIPT_FILE = "data/transcripts/meeting_1.json"
    chunk_transcript(TRANSCRIPT_FILE)