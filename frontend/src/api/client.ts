import axios, { AxiosInstance } from 'axios'

const API_KEY = import.meta.env.VITE_APP_API_KEY || ''
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const client: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add Authorization header to every request (except /health which needs no auth)
client.interceptors.request.use((config) => {
  // All endpoints except /health require the Authorization header per contract §1.5
  if (config.url !== '/health') {
    config.headers.Authorization = `Bearer ${API_KEY}`
  }
  return config
})

export default client

