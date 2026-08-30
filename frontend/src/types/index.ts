/**
 * TypeScript types matching the Project_Data_Contract.md
 * All field names are snake_case per contract §0
 */

// ===== Meeting Types (Contract §2.1) =====
export type MeetingStatus = 
  | 'uploaded' 
  | 'transcribing' 
  | 'transcribed' 
  | 'segmented' 
  | 'ready' 
  | 'failed'

export interface Meeting {
  meeting_id: string  // format: "meeting_{n}" (e.g. "meeting_1")
  title: string
  date: string        // ISO format: "2026-09-08"
  audio_url: string
  duration_seconds: number
  status: MeetingStatus
}

export interface MeetingListResponse {
  meetings: Meeting[]
}

// ===== Transcript Types (Contract §2.2) =====
export interface Utterance {
  speaker: string
  start_time: number  // seconds
  end_time: number    // seconds
  text: string
}

export interface TranscriptOutput {
  meeting_id: string
  utterances: Utterance[]
}

// ===== Segment Types (Contract §2.3) =====
export interface Segment {
  segment_id: string  // format: "m{meetingNumber}_s{segmentNumber}" (e.g. "m2_s08")
  meeting_id: string
  start_time: number  // seconds
  end_time: number    // seconds
  speaker: string
  topic: string
  summary: string
  decision_text: string | null  // null if not a decision
  segment_text: string
}

export interface SegmentListResponse {
  meeting_id: string
  segments: Segment[]
}

// ===== Retrieval Types (Contract §2.4) =====
export interface RetrievalQuery {
  query: string
  top_k?: number  // default 5
}

export interface RetrievalResult {
  segment_id: string
  meeting_id: string
  score: number          // cosine similarity, 0.0-1.0, rounded to 2 decimals
  start_time: number     // seconds
  end_time: number       // seconds
  topic: string
  summary: string
  decision_text: string | null
  segment_text: string
}

export interface RetrievalOutput {
  query: string
  top_k: number
  results: RetrievalResult[]
}

// ===== Answer Types (Contract §2.5) =====
export interface Evidence {
  segment_id: string
  meeting_id: string
  meeting_title: string
  start_time: number      // seconds (source of truth)
  timestamp: string       // mm:ss format (derived for display)
  change: string
}

export interface FinalAnswerOutput {
  question: string
  status: 'resolved' | 'unresolved'
  final_decision: string | null  // null if unresolved
  answer: string                  // exact string for TTS, speakable, no markdown
  evidence: Evidence[]            // sorted chronologically by start_time ascending
}

export interface AnswerQuery {
  question: string
}

// ===== Error Types (Contract §1) =====
export interface ErrorResponse {
  error: true
  code: 'UNAUTHORIZED' | 'VALIDATION_ERROR' | 'NOT_FOUND' | 'NOT_READY' | 'UPSTREAM_ERROR' | 'INTERNAL_ERROR'
  message: string
}

export interface HealthResponse {
  status: 'ok'
}
