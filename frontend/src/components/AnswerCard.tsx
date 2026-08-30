import React from 'react'

interface AnswerCardProps {
  question: string
  answer: string
  score?: number
}

export default function AnswerCard({ question, answer, score }: AnswerCardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-4 mb-4">
      <h3 className="font-bold text-lg mb-2">{question}</h3>
      <p className="text-gray-700 mb-2">{answer}</p>
      {score !== undefined && (
        <div className="text-sm text-gray-500">Confidence: {(score * 100).toFixed(1)}%</div>
      )}
    </div>
  )
}
