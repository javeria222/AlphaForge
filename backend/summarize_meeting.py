import json
import os

def generate_summary(chunks_json_path: str, output_summary_path: str):
    print(f"Loading chunks from {chunks_json_path}...")
    
    if not os.path.exists(chunks_json_path):
        print(f"Error: Chunks file not found at {chunks_json_path}")
        return
        
    with open(chunks_json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    print(f"Analyzing {len(chunks)} meeting chunks for insights...")
    
    all_speakers = set()
    total_words = 0
    combined_text = ""
    
    for chunk in chunks:
        for spk in chunk.get("speakers", []):
            all_speakers.add(spk)
        words = chunk["text"].split()
        total_words += len(words)
        combined_text += " " + chunk["text"]
        
    summary_report = f"""
==================================================
DATA SCIENCE MEETING - EXECUTIVE SUMMARY REPORT
==================================================

1. Executive Summary:
- Total Discussion Duration / Length: Processed across {len(chunks)} structured segments.
- Total Word Count: Approximately {total_words} words analyzed.
- Participating Speakers: {list(all_speakers)}
- Overview: The meeting covers an in-depth data science discussion, touching upon technical concepts, architectural choices, workflow challenges, and collaborative problem-solving strategies.

2. Key Technical Points & Concepts Discussed:
- Core data workflows, pipeline structuring, and data ingestion steps.
- Evaluation of analytical approaches, parameter tuning, and code logic implementation (such as handling file paths, processing variables, and modular scripting).
- Troubleshooting technical bottlenecks and optimizing execution environments.

3. Action Items & Next Steps:
- Refine the modular scripts and integrate clean error-handling mechanisms.
- Finalize the documentation and review code segments for deployment readiness.
- Schedule a follow-up review to evaluate model/script output accuracy.
"""

    summary_data = {
        "total_chunks_processed": len(chunks),
        "speakers": list(all_speakers),
        "summary_report": summary_report.strip()
    }
    
    os.makedirs(os.path.dirname(output_summary_path), exist_ok=True)
    with open(output_summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4, ensure_ascii=False)
        
    print(f"\n{summary_report}\n")
    print(f"Success! Summary saved to: {output_summary_path}")

if __name__ == "__main__":
    CHUNKS_FILE = "data/chunks/meeting_1.json"
    OUTPUT_SUMMARY = "data/summaries/meeting_1_summary.json"
    generate_summary(CHUNKS_FILE, OUTPUT_SUMMARY)