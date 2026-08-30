import React, { useState } from 'react'

interface Decision {
  id: number
  title: string
  description: string
  timestamp: string
}

export default function DecisionTimeline() {
  const [decisions, setDecisions] = useState<Decision[]>([])

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">Decision Timeline</h2>
      
      {decisions.length === 0 ? (
        <p className="text-gray-500">No decisions extracted yet.</p>
      ) : (
        <div className="space-y-4">
          {decisions.map((decision) => (
            <div key={decision.id} className="border-l-4 border-blue-500 pl-4">
              <h3 className="font-bold">{decision.title}</h3>
              <p className="text-gray-700">{decision.description}</p>
              <span className="text-sm text-gray-500">{decision.timestamp}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
