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
        
        # Split text into sentences cleanly
        for sentence in text.replace('!', '.').replace('?', '.').split('.'):
            clean_s = sentence.strip()
            if len(clean_s.split()) > 3:  # ignore micro-fragments
                all_sentences.append(clean_s)
                
    clean_combined_text = combined_text.strip()
    overview_snippet = clean_combined_text[:400] + "..." if len(clean_combined_text) > 400 else clean_combined_text
    
    # 1. Smarter Key Point Selection (Scoring based on substance, nouns, and core discussion cues)
    scored_sentences = []
    filler_starters = ('yeah', 'okay', 'so,', 'um', 'uh', 'right', 'i mean', 'well')
    
    for s in all_sentences:
        s_lower = s.lower()
        if s_lower.startswith(filler_starters):
            continue
            
        score = 0
        word_count = len(s.split())
        
        # Reward optimal sentence length (not too short, not a giant run-on paragraph)
        if 6 <= word_count <= 25:
            score += 2
            
        # Reward sentences containing summary or focal indicators
        focal_cues = ['important', 'critical', 'main', 'conclusion', 'decision', 'result', 'issue', 'problem', 'agree', 'focus']
        if any(cue in s_lower for cue in focal_cues):
            score += 3
            
        scored_sentences.append((score, s))
        
    # Sort by calculated importance score rather than raw length
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    top_key_points = [item[1] for item in scored_sentences[:3]]
    
    key_points = "\n".join([f"- {kp}." for kp in top_key_points]) if top_key_points else "- No substantial key points found in the transcript."
    
    # 2. Ultra-Strict Action Item Extraction (Targeting only true assignments)
    strict_action_triggers = [
        'action item', 'todo', 'task', 'assigned to', 
        'responsible for', 'take care of', 'look into', 
        'please make sure', 'let us ensure', 'next step'
    ]
    
    negation_words = ["don't", 'do not', "doesn't", 'not', 'no ', 'never']
    noise_words = ['thanks', 'thank you', 'person', 'tangerine']
    
    action_candidates = []
    for s in all_sentences:
        s_lower = s.lower()
        
        has_trigger = any(trigger in s_lower for trigger in strict_action_triggers)
        has_negation = any(neg in s_lower for neg in negation_words)
        has_noise = any(noise in s_lower for noise in noise_words)
        
        if has_trigger and not has_negation and not has_noise:
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