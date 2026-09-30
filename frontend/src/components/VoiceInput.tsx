import React, { useState, useRef } from 'react'

export interface VoiceInputProps {
  question: string
  isLoading: boolean
  onQuestionChange: (value: string) => void
  onSubmit: (nextQuestion: string) => Promise<void>
  onVoiceSubmit: (audio: Blob) => Promise<void>
}

const examples = [
  'What did we finally decide about the database?',
  'What did we decide about the API redesign?',
  'How did our authentication decision evolve?',
]

export default function VoiceInput({
  question,
  isLoading,
  onQuestionChange,
  onSubmit,
  onVoiceSubmit,
}: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      chunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' })
        
        // Pass audio blob to parent
        await onVoiceSubmit(audioBlob)

        // Stop media tracks to release microphone hardware
        stream.getTracks().forEach((track) => track.stop())
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (err) {
      console.error('Microphone access denied or error:', err)
      alert('Could not access microphone. Please check permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

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
          disabled={isLoading || isRecording}
        />

        <div className="form-actions">
          <button type="submit" className="primary-button" disabled={isLoading || isRecording || !question.trim()}>
            {isLoading ? 'Thinking...' : 'Ask memory'}
            <span aria-hidden="true">&#8594;</span>
          </button>

          <button
            type="button"
            className={`voice-button ${isRecording ? 'is-recording' : ''}`}
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isLoading}
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
          <button key={example} type="button" onClick={() => onSubmit(example)} disabled={isLoading || isRecording}>
            {example}
          </button>
        ))}
      </div>

      <p className="voice-note">
        Voice capture is active. Recorded audio will be processed upon stopping.
      </p>
    </section>
  )
}