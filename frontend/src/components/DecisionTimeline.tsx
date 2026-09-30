import type { Evidence } from '../types'

interface DecisionTimelineProps {
  evidence: Evidence[]
  selectedEvidence: Evidence | null
  onSelect: (evidence: Evidence) => void
}

export default function DecisionTimeline({ evidence, selectedEvidence, onSelect }: DecisionTimelineProps) {
  const sortedEvidence = [...evidence].sort((left, right) => left.start_time - right.start_time)

  return (
    <section className="timeline-card" aria-labelledby="timeline-heading">
      <div className="timeline-heading">
        <div>
          <div className="section-kicker">Evidence trail</div>
          <h2 id="timeline-heading">Decision timeline</h2>
        </div>
        {sortedEvidence.length > 0 && <span className="evidence-count">{sortedEvidence.length} moments</span>}
      </div>
      {sortedEvidence.length === 0 ? (
        <div className="timeline-empty">Evidence will appear after a question is answered.</div>
      ) : (
        <div className="timeline-list">
          {sortedEvidence.map((item, index) => {
            const isSelected = selectedEvidence?.segment_id === item.segment_id
            return (
              <button
                type="button"
                className={`timeline-item ${isSelected ? 'is-selected' : ''}`}
                key={item.segment_id}
                onClick={() => onSelect(item)}
                aria-current={isSelected ? 'true' : undefined}
              >
                <span className="timeline-marker" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
                <span className="timeline-content">
                  <span className="timeline-meta">{item.meeting_title} <strong>{item.timestamp}</strong></span>
                  <span className="timeline-change">{item.change}</span>
                  <span className="timeline-id">{item.meeting_id} / {item.segment_id}</span>
                </span>
                <span className="timeline-arrow" aria-hidden="true">&#8599;</span>
              </button>
            )
          })}
        </div>
      )}
    </section>
  )
}
