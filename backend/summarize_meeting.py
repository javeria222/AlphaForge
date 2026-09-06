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
    all_sentences = []
    
    for chunk in chunks:
        for spk in chunk.get("speakers", []):
            all_speakers.add(spk)
        text = chunk["text"].strip()
        words = text.split()
        total_words += len(words)
        combined_text += " " + text
        
        for sentence in text.replace('!', '.').replace('?', '.').split('.'):
            clean_s = sentence.strip()

            if len(clean_s.split()) > 4:
                all_sentences.append(clean_s)
                
    clean_combined_text = combined_text.strip()
    overview_snippet = clean_combined_text[:400] + "..." if len(clean_combined_text) > 400 else clean_combined_text
    
    substantive_sentences = [
        s for s in all_sentences 
        if not s.lower().startswith(('yeah', 'okay', 'so,', 'um', 'uh', 'right'))
    ]
    
    sorted_by_length = sorted(substantive_sentences, key=len, reverse=True)
    key_points_list = sorted_by_length[:3] if len(sorted_by_length) >= 3 else all_sentences[:3]
    key_points = "\n".join([f"- {kp}." for kp in key_points_list]) if key_points_list else "- No substantial key points found in the transcript."
    
    action_keywords = ['need to', 'have to', 'must', 'action', 'todo', 'task', 'going to', 'will implement', 'please fix', 'make sure']
    action_candidates = []
    
    for s in all_sentences:
        s_lower = s.lower()
        if any(kw in s_lower for kw in action_keywords):
            if s not in action_candidates:
                action_candidates.append(s)
                
    action_items_list = action_candidates[:3] if action_candidates else []
    action_items = "\n".join([f"- {ai}." for ai in action_items_list]) if action_items_list else "- No explicit action items recorded in this segment."

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