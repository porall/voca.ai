// Dashboard page - user management area
import { useState, useEffect } from 'react'
import { getMe, getToken, removeToken, type User } from '../api/auth'
import { listVoices, type Voice } from '../api/voices'
import { listProjects, type Project } from '../api/projects'
import { useNavigate, Link } from 'react-router-dom'
import Header from '../components/Header'

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null)
  const [voices, setVoices] = useState<Voice[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const token = getToken()
    if (!token) {
      navigate('/login')
      return
    }

    Promise.all([
      getMe(token),
      listVoices(),
      listProjects()
    ])
      .then(([userData, voicesData, projectsData]) => {
        setUser(userData)
        setVoices(voicesData)
        setProjects(projectsData)
      })
      .catch((err) => {
        console.error('[Dashboard] Error:', err);
        setError(err.message || '加载失败，请重试');
      })
      .finally(() => setLoading(false))
  }, [navigate])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900 flex items-center justify-center">
        <div className="text-white text-xl">加载中...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900">
      <Header showLogout />
      <main className="px-8 py-8">
        {error && (
          <div className="max-w-4xl mx-auto mb-4 p-4 bg-red-500/20 border border-red-500 rounded-lg">
            <p className="text-red-200">{error}</p>
            <button 
              onClick={() => { removeToken(); navigate('/login') }}
              className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              重新登录
            </button>
          </div>
        )}
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-2">欢迎，{user?.nickname || user?.email}！</h2>
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
              <Link to="/song-create" className="inline-block px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                开始创作
              </Link>
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

          {/* Projects List */}
          {projects.length > 0 && (
            <div className="mt-8">
              <h3 className="text-xl font-semibold text-white mb-4">我的创作</h3>
              <div className="space-y-3">
                {projects.slice(0, 5).map(project => (
                  <div key={project.id} className="bg-white/5 p-4 rounded-lg flex items-center justify-between">
                    <div>
                      <p className="text-white font-medium">{project.name}</p>
                      <p className="text-purple-300 text-sm">
                        状态: {project.status === 'completed' ? '✅ 完成' : 
                              project.status === 'processing' ? '🎵 生成中' :
                              project.status === 'failed' ? '❌ 失败' : '📝 草稿'}
                      </p>
                    </div>
                    {project.status === 'completed' && (
                      <div className="flex gap-2">
                        <Link to={`/music-player?id=${project.id}`} className="px-3 py-1 bg-purple-600 text-white rounded-lg text-sm hover:bg-purple-700">
                          预览
                        </Link>
                        {project.music_url && (
                          <a
                            href={project.music_url}
                            download={project.name + '.mp3'}
                            className="px-3 py-1 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700"
                          >
                            ⬇️
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
              {projects.length > 5 && (
                <Link to="/projects" className="block text-center text-purple-300 mt-4 hover:text-white">
                  查看全部 {projects.length} 个作品 →
                </Link>
              )}
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