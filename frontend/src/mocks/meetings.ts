import type { Meeting } from '../types'

export const mockMeetings: Meeting[] = [
  {
    meeting_id: 'meeting_1',
    title: 'Kickoff - Architecture Planning',
    date: '2026-09-01',
    audio_url: '',
    duration_seconds: 900,
    status: 'ready',
  },
  {
    meeting_id: 'meeting_2',
    title: 'Backend Sync - Database Discussion',
    date: '2026-09-08',
    audio_url: '',
    duration_seconds: 900,
    status: 'ready',
  },
  {
    meeting_id: 'meeting_3',
    title: 'Final Review',
    date: '2026-09-15',
    audio_url: '',
    duration_seconds: 1200,
    status: 'ready',
  },
]
