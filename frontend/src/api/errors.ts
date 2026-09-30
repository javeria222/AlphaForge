import axios from 'axios'
import type { ErrorResponse } from '../types'

interface FastApiErrorEnvelope {
  detail?: ErrorResponse | Array<{ msg?: string }>
}

export function getUserFacingError(error: unknown): string {
  if (axios.isAxiosError<ErrorResponse | FastApiErrorEnvelope>(error)) {
    const responseData = error.response?.data
    const detail = responseData && 'detail' in responseData ? responseData.detail : undefined
    const apiError = responseData && 'error' in responseData && responseData.error
      ? responseData
      : detail && !Array.isArray(detail)
        ? detail
        : undefined
    const code = apiError?.code

    if (code === 'UNAUTHORIZED') return 'The API key was not accepted. Check your frontend environment settings.'
    if (code === 'NOT_READY') return 'This meeting is still being processed. Try again shortly.'
    if (code === 'NOT_FOUND') return 'That meeting memory could not be found.'
    if (code === 'VALIDATION_ERROR') return 'Please enter a more specific question.'
    if (code === 'UPSTREAM_ERROR') return 'The answer service is temporarily unavailable.'
    if (Array.isArray(detail)) return 'The request format was invalid. Please enter a more specific question.'
  }

  return 'The meeting memory could not answer that right now. Please try again.'
}
