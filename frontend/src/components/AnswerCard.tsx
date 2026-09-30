import type { FinalAnswerOutput } from '../types'

interface AnswerCardProps {
  answer: FinalAnswerOutput | null
}

export default function AnswerCard({ answer }: AnswerCardProps) {
  if (!answer) {
    return (
      <section className="answer-card empty-card" aria-labelledby="answer-heading">
        <div className="section-kicker">Answer</div>
        <h2 id="answer-heading">Your answer will appear here.</h2>
        <p>Ask a question to search the meeting memory.</p>
      </section>
    )
  }

  return (
    <section className="answer-card" aria-labelledby="answer-heading">
      <div className="answer-topline">
        <div className="section-kicker">Answer</div>
        <span className={`status-badge ${answer.status}`}>{answer.status}</span>
      </div>
      <p className="asked-question">“{answer.question}”</p>
      <h2 id="answer-heading">{answer.final_decision || 'Decision not resolved'}</h2>
      <p className="answer-copy">{answer.answer}</p>
      {answer.status === 'unresolved' && <p className="muted-note">No final decision is shown because the available evidence is inconclusive.</p>}
    </section>
  )
}
