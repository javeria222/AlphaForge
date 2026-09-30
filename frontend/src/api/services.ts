/**
 * API service functions for the Conversation Memory Voice Agent frontend
 * All requests include Authorization: Bearer header per contract §1.5
 * All endpoints use snake_case keys per contract §0
 */
import axios from 'axios'
import client from './client'
import type {
  Meeting,
  MeetingListResponse,
  TranscriptOutput,
  SegmentListResponse,
  RetrievalOutput,
  FinalAnswerOutput,
  HealthResponse,
} from '../types'
import { getMockAnswer, mockMeetings } from '../mocks'

/**
 * Health check endpoint (no auth required)
 * GET /health
 */
export const checkHealth = async (): Promise<HealthResponse> => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const healthUrl = apiUrl.endsWith('/api') ? `${apiUrl.slice(0, -4)}/health` : `${apiUrl}/health`
  const response = await axios.get<HealthResponse>(healthUrl)
  return response.data
}

// ===== Meetings API =====

/**
 * Create a new meeting
 * POST /meetings
 */
export const createMeeting = async (
  title: string,
  date: string,
  audio_url: string,
  duration_seconds: number
): Promise<Meeting> => {
  const response = await client.post<Meeting>('/meetings', {
    title,
    date,
    audio_url,
    duration_seconds,
  })
  return response.data
}

/**
 * List all meetings
 * GET /meetings
 */
export const listMeetings = async (): Promise<MeetingListResponse> => {
  const response = await client.get<MeetingListResponse>('/meetings')
  return response.data
}

export const listMockMeetings = (): MeetingListResponse => ({
  meetings: mockMeetings,
})

/**
 * Get a single meeting by ID
 * GET /meetings/{meeting_id}
 */
export const getMeeting = async (meeting_id: string): Promise<Meeting> => {
  const response = await client.get<Meeting>(`/meetings/${encodeURIComponent(meeting_id)}`)
  return response.data
}

/**
 * Get transcript for a meeting
 * GET /meetings/{meeting_id}/transcript
 */
export const getTranscript = async (meeting_id: string): Promise<TranscriptOutput> => {
  const response = await client.get<TranscriptOutput>(`/meetings/${encodeURIComponent(meeting_id)}/transcript`)
  return response.data
}

/**
 * Get segments for a meeting
 * GET /meetings/{meeting_id}/segments
 */
export const getSegments = async (meeting_id: string): Promise<SegmentListResponse> => {
  const response = await client.get<SegmentListResponse>(`/meetings/${encodeURIComponent(meeting_id)}/segments`)
  return response.data
}

// ===== Search API =====

/**
 * Search across all meetings
 * POST /search
 */
export const searchMeetings = async (query: string, top_k?: number): Promise<RetrievalOutput> => {
  const response = await client.post<RetrievalOutput>('/search', {
    query,
    top_k: top_k ?? 5,
  })
  return response.data
}

/**
 * Get answer to a question (retrieval + reasoning)
 * POST /answer
 */
export const getAnswerFromApi = async (question: string): Promise<FinalAnswerOutput> => {
  const response = await client.post<FinalAnswerOutput>('/answer', {
    question,
  })
  return response.data
}

export const getAnswer = async (question: string): Promise<FinalAnswerOutput> => {
  if (import.meta.env.VITE_USE_MOCK_API === 'true') {
    await new Promise((resolve) => window.setTimeout(resolve, 650))
    return getMockAnswer(question)
  }

  return getAnswerFromApi(question)
}

// ===== Voice Agent API =====

/**
 * Voice agent tool endpoint
 * POST /voice/tool/search_meeting_memory
 * Same as /answer but for voice agent tool invocation
 */
export const voiceSearchMemory = async (question: string): Promise<FinalAnswerOutput> => {
  const response = await client.post<FinalAnswerOutput>('/voice/tool/search_meeting_memory', {
    question,
  })
  return response.data
}
