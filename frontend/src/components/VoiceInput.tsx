import { useState } from 'react'

interface VoiceInputProps {
  question: string
  isLoading: boolean
  onQuestionChange: (question: string) => void
  onSubmit: (question: string) => void
}

const examples = [
  'What did we finally decide about the database?',
  'What did we decide about the API redesign?',
  'How did our authentication decision evolve?',
]

export default function VoiceInput({ question, isLoading, onQuestionChange, onSubmit }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false)

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (question.trim()) onSubmit(question.trim())
  }

  return (
    <section className="ask-panel" aria-labelledby="ask-heading">
      <div className="eyebrow">Meeting memory</div>
      <h2 id="ask-heading">Ask your past conversations.</h2>
      <p className="panel-copy">Search across meetings and follow the decision trail back to its source.</p>
      <form onSubmit={handleSubmit} className="question-form">
        <label htmlFor="question">Your question</label>
        <textarea
          id="question"
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="What did we finally decide about the database?"
          rows={4}
          disabled={isLoading}
        />
        <div className="form-actions">
          <button type="submit" className="primary-button" disabled={isLoading || !question.trim()}>
            {isLoading ? 'Thinking...' : 'Ask memory'}
            <span aria-hidden="true">&#8594;</span>
          </button>
          <button
            type="button"
            className={`voice-button ${isRecording ? 'is-recording' : ''}`}
            onClick={() => setIsRecording((recording) => !recording)}
            aria-pressed={isRecording}
            aria-label={isRecording ? 'Stop voice input' : 'Start voice input'}
          >
            <span aria-hidden="true">{isRecording ? '■' : '◉'}</span>
            {isRecording ? 'Listening...' : 'Voice input'}
          </button>
        </div>
      </form>
      <div className="example-list" aria-label="Example questions">
        <span>Try</span>
        {examples.map((example) => (
          <button key={example} type="button" onClick={() => onSubmit(example)} disabled={isLoading}>
            {example}
          </button>
        ))}
      </div>
      <p className="voice-note">Voice capture is staged for the managed voice agent. Text input is ready for the mock experience.</p>
    </section>
  )
}
