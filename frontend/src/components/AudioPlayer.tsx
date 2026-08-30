import React from 'react'

interface AudioPlayerProps {
  url: string
}

export default function AudioPlayer({ url }: AudioPlayerProps) {
  return (
    <div className="mt-4">
      <audio controls className="w-full">
        <source src={url} type="audio/wav" />
        Your browser does not support the audio element.
      </audio>
    </div>
  )
}
