import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { uploadVoice } from '../api/voices'
import './VoiceUpload.css'

export default function VoiceUpload() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!file) {
      setError('Please select an audio file')
      return
    }

    if (!name.trim()) {
      setError('Please enter a voice name')
      return
    }

    setUploading(true)
    try {
      const result = await uploadVoice(name, file)
      setSuccess(`Voice "${result.name}" uploaded successfully!`)
      setName('')
      setFile(null)
      // Reset file input
      const fileInput = document.getElementById('audio-file') as HTMLInputElement
      if (fileInput) fileInput.value = ''
    } catch (err: any) {
      setError(err.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="voice-upload-page">
      <div className="voice-upload-card">
        <h1>Clone Your Voice</h1>
        <p className="subtitle">
          Upload a recording of your voice to create an AI clone
        </p>

        <form onSubmit={handleSubmit} className="voice-upload-form">
          <div className="form-group">
            <label htmlFor="voice-name">Voice Name</label>
            <input
              id="voice-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="My Singing Voice"
              disabled={uploading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="audio-file">Audio File (MP3, WAV, M4A)</label>
            <input
              id="audio-file"
              type="file"
              accept=".mp3,.wav,.m4a,.flac,audio/*"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              disabled={uploading}
            />
            <span className="help-text">5-30 seconds of you singing works best</span>
          </div>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <button
            type="submit"
            className="submit-btn"
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Upload & Clone'}
          </button>
        </form>

        <div className="nav-links">
          <button onClick={() => navigate('/dashboard')}>
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}