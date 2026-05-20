// Dashboard page - user management area
import { useState, useEffect } from 'react'
import { getMe, getToken, removeToken, type User } from '../api/auth'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const token = getToken()
    if (!token) {
      navigate('/login')
      return
    }

    getMe(token)
      .then(setUser)
      .catch(() => {
        removeToken()
        navigate('/login')
      })
      .finally(() => setLoading(false))
  }, [navigate])

  const handleLogout = () => {
    removeToken()
    navigate('/login')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900">
      {/* Header */}
      <header className="flex items-center justify-between px-8 py-4">
        <h1 className="text-2xl font-bold text-white">🎤 Voca.ai</h1>
        <button
          onClick={handleLogout}
          className="px-4 py-2 text-white hover:text-purple-200"
        >
          Logout
        </button>
      </header>

      {/* Main content */}
      <main className="px-8 py-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-2">Welcome, {user?.nickname || user?.email}!</h2>
          <p className="text-purple-200 mb-8">Start creating your AI music</p>

          {/* Quick actions */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Voice Cloning */}
            <div className="bg-white/10 p-6 rounded-xl">
              <div className="text-3xl mb-4">🎙️</div>
              <h3 className="text-xl font-semibold text-white mb-2">Clone Your Voice</h3>
              <p className="text-purple-200 mb-4">
                Upload a 30-second audio sample to create your voice clone.
              </p>
              <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                Upload Audio
              </button>
            </div>

            {/* Create Song */}
            <div className="bg-white/10 p-6 rounded-xl">
              <div className="text-3xl mb-4">🎵</div>
              <h3 className="text-xl font-semibold text-white mb-2">Create New Song</h3>
              <p className="text-purple-200 mb-4">
                Describe your song and let AI generate the music.
              </p>
              <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                Start Creating
              </button>
            </div>
          </div>

          {/* Premium badge */}
          {user?.is_premium && (
            <div className="mt-8 p-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl">
              <p className="text-white font-semibold">✨ You're a Premium member!</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}