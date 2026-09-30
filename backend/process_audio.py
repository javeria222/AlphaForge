import os
import json
from dotenv import load_dotenv
import assemblyai as aai

load_dotenv()

api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not api_key:
    raise ValueError("ASSEMBLYAI_API_KEY is missing! Please check your .env file.")

aai.settings.api_key = api_key

def transcribe_local_audio(audio_path: str, meeting_id: str, output_json_path: str):
    print(f"[{meeting_id}] Uploading local audio to AssemblyAI for transcription and speaker diarization...")
    
    config = aai.TranscriptionConfig(speaker_labels=True)
    
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(audio_path, config=config, poll_timeout=600)
    
    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed for {meeting_id}: {transcript.error}")
        return
    
    formatted_segments = []
    
    for utterance in transcript.utterances:
        segment = {
            "meeting_id": meeting_id,
            "speaker": f"Speaker {utterance.speaker}", 
            "start_time": utterance.start // 1000,
            "end_time": max(utterance.start // 1000, utterance.end // 1000),            
            "text": utterance.text                    
        }
        formatted_segments.append(segment)
    
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(formatted_segments, f, indent=4, ensure_ascii=False)
        
    print(f"Success! Transcript saved to: {output_json_path}")

if __name__ == "__main__":
    for n in (1, 2, 3):
        meeting_id = f"meeting_{n}"
        audio_file = f"data/audio/{meeting_id}.mp3"
        output_file = f"data/transcripts/{meeting_id}.json"
        if os.path.exists(audio_file):
            transcribe_local_audio(audio_file, meeting_id=meeting_id, output_json_path=output_file)
        else:
            print(f"Skipping {meeting_id}: '{audio_file}' not found. Run make_audio.py first.")