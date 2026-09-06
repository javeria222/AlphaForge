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

    transcript = transcriber.transcribe(audio_path, config=config)
    
    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed for {meeting_id}: {transcript.error}")
        return
    
    formatted_segments = []
    
    for utterance in transcript.utterances:
        segment = {
            "meeting_id": meeting_id,
            "speaker": f"Speaker {utterance.speaker}", 
            "start_time": utterance.start,           
            "end_time": utterance.end,                
            "text": utterance.text                    
        }
        formatted_segments.append(segment)
    
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(formatted_segments, f, indent=4, ensure_ascii=False)
        
    print(f"Success! Transcript saved to: {output_json_path}")

if __name__ == "__main__":

    AUDIO_FILE = "data/audio/meeting_1.mp3"
    OUTPUT_FILE = "data/transcripts/meeting_1.json"
    
    if os.path.exists(AUDIO_FILE):
        transcribe_local_audio(AUDIO_FILE, meeting_id="meeting_1", output_json_path=OUTPUT_FILE)
    else:
        print(f"Error: Audio file not found at '{AUDIO_FILE}'. Please place your audio file in the 'backend/data/audio/' folder.")