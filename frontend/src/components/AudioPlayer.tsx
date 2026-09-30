import { useEffect, useRef, useState } from 'react'

interface AudioPlayerProps {
  url?: string
  seekTo?: number
  meetingTitle?: string
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60)
  const remainder = Math.floor(seconds % 60).toString().padStart(2, '0')
  return `${minutes}:${remainder}`
}

export default function AudioPlayer({ url, seekTo, meetingTitle }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)

  useEffect(() => {
    if (audioRef.current && seekTo !== undefined && url) {
      audioRef.current.currentTime = seekTo
      setCurrentTime(seekTo)
    }
  }, [seekTo, url])

  return (
    <section className="audio-card" aria-labelledby="audio-heading">
      <div className="audio-header">
        <div>
          <div className="section-kicker">Source audio</div>
          <h2 id="audio-heading">{meetingTitle || 'Meeting recording'}</h2>
        </div>
        <span className="audio-time">{formatTime(currentTime)} / {formatTime(duration)}</span>
      </div>
      {url ? (
        <>
          <audio
            ref={audioRef}
            src={url}
            onLoadedMetadata={(event) => setDuration(event.currentTarget.duration)}
            onTimeUpdate={(event) => setCurrentTime(event.currentTarget.currentTime)}
            controls
          >
            Your browser does not support audio playback.
          </audio>
          <input
            className="audio-progress"
            type="range"
            min="0"
            max={duration || 0}
            value={Math.min(currentTime, duration || 0)}
            onChange={(event) => {
              const nextTime = Number(event.target.value)
              if (audioRef.current) audioRef.current.currentTime = nextTime
              setCurrentTime(nextTime)
            }}
            aria-label="Seek through meeting audio"
          />
        </>
      ) : (
        <div className="audio-empty">Audio is not attached to this mock meeting yet. Evidence selection still records the exact source timestamp.</div>
      )}
    </section>
  )
}
