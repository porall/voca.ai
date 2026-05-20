import { getToken } from './auth'

const API_URL = import.meta.env.VITE_API_URL || ''

export interface Voice {
  id: string
  name: string
  audio_url: string | null
  duration_secs: number | null
  is_default: boolean
  status: string
  created_at: string
}

export async function uploadVoice(name: string, file: File): Promise<Voice> {
  const formData = new FormData()
  formData.append('name', name)
  formData.append('file', file)

  const response = await fetch(`${API_URL}/api/voices/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${getToken()}`,
    },
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }))
    throw new Error(error.detail || 'Upload failed')
  }

  return response.json()
}

export async function listVoices(): Promise<Voice[]> {
  const response = await fetch(`${API_URL}/api/voices`, {
    headers: {
      'Authorization': `Bearer ${getToken()}`,
    },
  })

  if (!response.ok) {
    throw new Error('Failed to fetch voices')
  }

  return response.json()
}

export async function deleteVoice(voiceId: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/voices/${voiceId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${getToken()}`,
    },
  })

  if (!response.ok) {
    throw new Error('Failed to delete voice')
  }
}