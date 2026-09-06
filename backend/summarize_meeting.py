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
    extracted_sentences = []
    
    for chunk in chunks:
        for spk in chunk.get("speakers", []):
            all_speakers.add(spk)
        text = chunk["text"].strip()
        words = text.split()
        total_words += len(words)
        combined_text += " " + text
        
        for sentence in text.split('.'):
            clean_s = sentence.strip()
            if len(clean_s) > 15:  # filter out too short fragments
                extracted_sentences.append(clean_s)
                
    clean_combined_text = combined_text.strip()
    
    overview_snippet = clean_combined_text[:400] + "..." if len(clean_combined_text) > 400 else clean_combined_text
    
    key_points_list = extracted_sentences[:3] if len(extracted_sentences) >= 3 else extracted_sentences
    key_points = "\n".join([f"- {kp}." for kp in key_points_list]) if key_points_list else "- Discussed core project requirements and technical implementation details."
    
    action_candidates = [s for s in extracted_sentences if any(keyword in s.lower() for keyword in ['need', 'fix', 'update', 'check', 'do', 'will', 'should', 'push', 'run'])]
    if not action_candidates and len(extracted_sentences) > 3:
        action_candidates = extracted_sentences[3:5]
        
    action_items_list = action_candidates[:2] if action_candidates else ["Review discussed code logic and file paths.", "Proceed with implementation and verify results."]
    action_items = "\n".join([f"- {ai}." for ai in action_items_list])

    summary_report = f"""
==================================================
DATA SCIENCE MEETING - EXECUTIVE SUMMARY REPORT
==================================================

1. Executive Summary:
- Total Discussion Length: {total_words} words across {len(chunks)} segments.
- Participating Speakers: {list(all_speakers)}
- Overview: {overview_snippet}

2. Key Technical Points & Concepts Discussed:
{key_points}

3. Action Items & Next Steps:
{action_items}
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