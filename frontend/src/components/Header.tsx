// Header component with logo and navigation
import { Link, useNavigate } from 'react-router-dom'
import { removeToken } from '../api/auth'

interface HeaderProps {
  showLogout?: boolean
}

export default function Header({ showLogout = false }: HeaderProps) {
  const navigate = useNavigate()

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
      {showLogout && (
        <button
          onClick={handleLogout}
          className="px-4 py-2 text-white hover:text-purple-200"
        >
          退出登录
        </button>
      )}
    </header>
  )
}