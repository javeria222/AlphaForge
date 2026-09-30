import type { FinalAnswerOutput } from '../types'

const databaseAnswer: FinalAnswerOutput = {
  question: 'What did we finally decide about the database?',
  status: 'resolved',
  final_decision: 'PostgreSQL',
  answer: 'The final decision was PostgreSQL. The team initially proposed PostgreSQL in Meeting 1. In Meeting 2 at 12:48, the decision changed to MongoDB. In Meeting 3 at 18:20, it changed back to PostgreSQL.',
  evidence: [
    {
      segment_id: 'm1_s03',
      meeting_id: 'meeting_1',
      meeting_title: 'Kickoff - Architecture Planning',
      start_time: 500,
      timestamp: '08:20',
      change: 'PostgreSQL proposed',
    },
    {
      segment_id: 'm2_s08',
      meeting_id: 'meeting_2',
      meeting_title: 'Backend Sync - Database Discussion',
      start_time: 768,
      timestamp: '12:28',
      change: 'PostgreSQL -> MongoDB',
    },
    {
      segment_id: 'm3_s05',
      meeting_id: 'meeting_3',
      meeting_title: 'Final Review',
      start_time: 1100,
      timestamp: '18:20',
      change: 'MongoDB -> PostgreSQL',
    },
  ],
}

const apiAnswer: FinalAnswerOutput = {
  question: 'What did we decide about the API redesign?',
  status: 'resolved',
  final_decision: 'Keep the existing REST boundary and version the new endpoints.',
  answer: 'The team decided to keep the existing REST boundary and version the new endpoints so the redesign could ship without breaking current clients.',
  evidence: [
    {
      segment_id: 'm1_s07',
      meeting_id: 'meeting_1',
      meeting_title: 'Kickoff - Architecture Planning',
      start_time: 660,
      timestamp: '11:00',
      change: 'REST boundary retained; versioning proposed',
    },
    {
      segment_id: 'm3_s02',
      meeting_id: 'meeting_3',
      meeting_title: 'Final Review',
      start_time: 420,
      timestamp: '07:00',
      change: 'Versioned endpoints confirmed',
    },
  ],
}

const unresolvedAnswer = (question: string): FinalAnswerOutput => ({
  question,
  status: 'unresolved',
  final_decision: null,
  answer: 'I could not find enough clear evidence in the meeting memory to identify a final decision.',
  evidence: [],
})

export function getMockAnswer(question: string): FinalAnswerOutput {
  const normalizedQuestion = question.toLowerCase()

  if (normalizedQuestion.includes('database') || normalizedQuestion.includes('mongodb')) {
    return { ...databaseAnswer, question }
  }

  if (normalizedQuestion.includes('api')) {
    return { ...apiAnswer, question }
  }

  return unresolvedAnswer(question)
}
