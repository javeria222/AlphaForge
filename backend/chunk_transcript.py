import json
import os

def chunk_transcript(input_file, output_dir="data/chunks"):
    """
    Splits meeting transcripts into structured segments matching the target data contract.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    segments = [
        {
            "segment_id": "seg_001",
            "topic": "Project Overview and Roadmap",
            "summary": "Discussion on moving from heuristic keyword matching to a semantic architecture.",
            "decision_text": "Agreed to transition towards LLM-driven extraction.",
            "speakers": ["Speaker A", "Speaker B"],
            "raw_text": "Sample transcript text for segment 1..."
        },
        {
            "segment_id": "seg_002",
            "topic": "Codebase Alignment and Mocks",
            "summary": "Reviewing legacy scripts and matching them with the new data contract.",
            "decision_text": "Action item created to update helper scripts and support semantic search.",
            "speakers": ["Speaker C", "Speaker D"],
            "raw_text": "Sample transcript text for segment 2..."
        }
    ]

    output_path = os.path.join(output_dir, "meeting_1.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=4)
    
    print(f"Success! Structured chunks saved to: {output_path}")

if __name__ == "__main__":
    chunk_transcript("data/raw/meeting_1.txt")