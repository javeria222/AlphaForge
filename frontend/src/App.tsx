import './App.css'
import { useState } from 'react'
import VoiceInput from './components/VoiceInput'
import DecisionTimeline from './components/DecisionTimeline'
import AnswerCard from './components/AnswerCard'
import AudioPlayer from './components/AudioPlayer'
import { getAnswer, getMeeting } from './api/services'
import { getUserFacingError } from './api/errors'
import { mockMeetings } from './mocks'
import type { Evidence, FinalAnswerOutput, Meeting } from './types'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState<FinalAnswerOutput | null>(null)
  const [selectedEvidence, setSelectedEvidence] = useState<Evidence | null>(null)
  const [selectedMeeting, setSelectedMeeting] = useState<Meeting | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAsk = async (nextQuestion: string) => {
    setQuestion(nextQuestion)
    setIsLoading(true)
    setError(null)
    setSelectedEvidence(null)
    setSelectedMeeting(null)

    try {
      const nextAnswer = await getAnswer(nextQuestion)
      setAnswer(nextAnswer)
    } catch (requestError) {
      console.error(requestError)
      setAnswer(null)
      setError(getUserFacingError(requestError))
    } finally {
      setIsLoading(false)
    }
  }

  const handleEvidenceSelect = async (evidence: Evidence) => {
    setSelectedEvidence(evidence)
    setError(null)

    try {
      const meeting = import.meta.env.VITE_USE_MOCK_API === 'true'
        ? mockMeetings.find((item) => item.meeting_id === evidence.meeting_id) || null
        : await getMeeting(evidence.meeting_id)
      setSelectedMeeting(meeting)
    } catch (requestError) {
      console.error(requestError)
      setSelectedMeeting(null)
      setError(getUserFacingError(requestError))
    }
  }

  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="header-inner">
          <a className="brand" href="/" aria-label="AlphaForge home">
            <span className="brand-mark" aria-hidden="true">AF</span>
            <span>AlphaForge</span>
          </a>
          <div className="header-context">
            <span className="connection-dot" aria-hidden="true" />
            {import.meta.env.VITE_USE_MOCK_API === 'true' ? 'Mock memory' : 'API memory'}
          </div>
        </div>
      </header>

      <main className="main-content">
        <section className="intro-block">
          <div>
            <div className="eyebrow">Conversation memory / 01</div>
            <h1>Find the thread<br /><em>behind the decision.</em></h1>
          </div>
          <p>Ask a natural question about your meetings. AlphaForge connects the final answer to the moments that shaped it.</p>
        </section>

        <div className="workspace-grid">
          <VoiceInput question={question} isLoading={isLoading} onQuestionChange={setQuestion} onSubmit={handleAsk} />
          <div className="results-column">
            {isLoading && <div className="loading-state" role="status"><span className="loading-line" /> Searching meeting memory...</div>}
            {error && <div className="error-state" role="alert"><strong>Could not complete the search.</strong><span>{error}</span></div>}
            <AnswerCard answer={answer} />
            <DecisionTimeline evidence={answer?.evidence || []} selectedEvidence={selectedEvidence} onSelect={handleEvidenceSelect} />
            <AudioPlayer url={selectedMeeting?.audio_url || undefined} seekTo={selectedEvidence?.start_time} meetingTitle={selectedMeeting?.title || selectedEvidence?.meeting_title} />
          </div>
        </div>
      </main>
      <footer className="site-footer">AlphaForge / Conversation Memory Voice Agent <span>Contract-aligned prototype</span></footer>
    </div>
  )
}

export default App
