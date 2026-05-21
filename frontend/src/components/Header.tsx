// Header component with logo and navigation
import { Link, useNavigate } from 'react-router-dom'
import { removeToken, getStoredUser, getToken, getMe } from '../api/auth'
import { useEffect, useState } from 'react'

interface HeaderProps {
  showLogout?: boolean
}

export default function Header({ showLogout = false }: HeaderProps) {
  const navigate = useNavigate()
  const [points, setPoints] = useState<number>(0)

  useEffect(() => {
    // Load user and points
    const loadUser = async () => {
      const storedUser = getStoredUser()
      if (storedUser?.points) {
        setPoints(storedUser.points)
      }
      // Optionally refresh from server
      const token = getToken()
      if (token) {
        try {
          const user = await getMe(token)
          setPoints(user.points)
        } catch (e) {
          // Ignore
        }
      }
    }
    loadUser()
  }, [])

  const handleLogout = () => {
    removeToken()
    navigate('/login')
  }

  return (
    <header className="flex items-center justify-between px-8 py-4">
      <Link to="/" className="flex items-center gap-2">
        <span className="text-2xl">🎤</span>
        <span className="text-xl font-bold text-white">Voca.ai</span>
      </Link>
      <div className="flex items-center gap-4">
        {showLogout && (
          <span className="text-yellow-400 font-medium">
            🎵 {points} 积分
          </span>
        )}
        {showLogout && (
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-white hover:text-purple-200"
          >
            退出登录
          </button>
        )}
      </div>
    </header>
  )
}