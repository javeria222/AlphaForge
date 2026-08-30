import React, { useState } from 'react'
import AudioPlayer from './AudioPlayer'

export default function VoiceInput() {
  const [isRecording, setIsRecording] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)

  const handleStartRecording = () => {
    setIsRecording(true)
  }

  const handleStopRecording = () => {
    setIsRecording(false)
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">Voice Input</h2>
      
      <div className="space-y-4">
        <button
          onClick={handleStartRecording}
          disabled={isRecording}
          className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded"
        >
          {isRecording ? 'Recording...' : 'Start Recording'}
        </button>
        
        {isRecording && (
          <button
            onClick={handleStopRecording}
            className="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
          >
            Stop Recording
          </button>
        )}
        
        {audioUrl && <AudioPlayer url={audioUrl} />}
      </div>
    </div>
  )
}
