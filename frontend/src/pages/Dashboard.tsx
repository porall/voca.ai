// Dashboard page - user management area
import { useState, useEffect } from 'react'
import { getMe, getToken, removeToken, type User } from '../api/auth'
import { listVoices, type Voice } from '../api/voices'
import { useNavigate, Link } from 'react-router-dom'

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null)
  const [voices, setVoices] = useState<Voice[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const token = getToken()
    if (!token) {
      navigate('/login')
      return
    }

    Promise.all([
      getMe(token),
      listVoices()
    ])
      .then(([userData, voicesData]) => {
        setUser(userData)
        setVoices(voicesData)
      })
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
              <h3 className="text-xl font-semibold text-white mb-2">克隆你的声音</h3>
              <p className="text-purple-200 mb-4">
                上传 30 秒音频样本，创建你的声音克隆。
              </p>
              <Link to="/voice-upload" className="inline-block px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                上传音频
              </Link>
            </div>

            {/* Create Song */}
            <div className="bg-white/10 p-6 rounded-xl">
              <div className="text-3xl mb-4">🎵</div>
              <h3 className="text-xl font-semibold text-white mb-2">创建新歌曲</h3>
              <p className="text-purple-200 mb-4">
                描述你的歌曲，AI 自动生成配乐。
              </p>
              <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                开始创作
              </button>
            </div>
          </div>

          {/* Voice List */}
          {voices.length > 0 && (
            <div className="mt-8">
              <h3 className="text-xl font-semibold text-white mb-4">已克隆的声音</h3>
              <div className="grid md:grid-cols-3 gap-4">
                {voices.map(voice => (
                  <div key={voice.id} className="bg-white/5 p-4 rounded-lg">
                    <p className="text-white font-medium">{voice.name}</p>
                    <p className="text-purple-300 text-sm">
                      状态: {voice.status === 'ready' ? '✅ 就绪' : '⏳ 处理中'}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

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