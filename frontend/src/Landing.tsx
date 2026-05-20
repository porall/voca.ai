// Landing page - homepage
import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getToken, getMe, removeToken, setStoredUser, getStoredUser, type User } from './api/auth';
import './index.css';

function Landing() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check login state on mount - try stored user first for fast render
    const storedUser = getStoredUser();
    if (storedUser) {
      setUser(storedUser);
      setLoading(false);
      return;
    }
    
    // Otherwise validate token
    const token = getToken();
    if (token) {
      getMe(token)
        .then((u) => {
          setUser(u);
          setStoredUser(u); // Cache for next time
        })
        .catch(() => {
          removeToken();
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogout = () => {
    removeToken();
    setUser(null);
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900">
      {/* Header */}
      <header className="flex items-center justify-between px-8 py-4">
        <Link to="/" className="text-2xl font-bold text-white hover:opacity-80">
          🎤 Voca.ai
        </Link>
        
        {user ? (
          // Logged in - show username and logout
          <nav className="flex gap-4 items-center">
            <span className="text-purple-200">Welcome, {user.nickname || user.email}</span>
            <Link 
              to="/dashboard"
              className="px-4 py-2 text-white hover:text-purple-200"
            >
              Dashboard
            </Link>
            <button 
              onClick={handleLogout}
              className="px-4 py-2 text-purple-300 hover:text-white"
            >
              Logout
            </button>
          </nav>
        ) : (
          // Not logged in - show Login and Get Started
          <nav className="flex gap-4">
            <Link to="/login" className="px-4 py-2 text-white hover:text-purple-200">
              Login
            </Link>
            <Link 
              to="/register"
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Get Started
            </Link>
          </nav>
        )}
      </header>

      {/* Hero */}
      <main className="flex flex-col items-center justify-center px-4 py-20 text-center">
        <h2 className="text-5xl font-bold text-white mb-6">
          Your Voice, Your Song
        </h2>
        <p className="text-xl text-purple-200 mb-8 max-w-2xl">
          Create AI-powered music with your own cloned voice. 
          Generate original songs and hear them sung in your unique voice.
        </p>
        {user ? (
          <Link 
            to="/dashboard"
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white 
                       text-lg font-semibold rounded-full hover:scale-105 transition-transform"
          >
            Go to Dashboard
          </Link>
        ) : (
          <Link 
            to="/register"
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white 
                       text-lg font-semibold rounded-full hover:scale-105 transition-transform"
          >
            Start Creating Free
          </Link>
        )}
        
        <p className="mt-4 text-purple-300 text-sm">
          No credit card required • 3 free songs/day
        </p>
      </main>

      {/* Features */}
      <section className="px-8 py-16 bg-white/5">
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="p-6 bg-white/10 rounded-xl">
            <div className="text-3xl mb-4">🎙️</div>
            <h3 className="text-xl font-semibold text-white mb-2">Voice Cloning</h3>
            <p className="text-purple-200">
              Upload a 30-second audio sample. We'll clone your unique voice.
            </p>
          </div>
          <div className="p-6 bg-white/10 rounded-xl">
            <div className="text-3xl mb-4">🎵</div>
            <h3 className="text-xl font-semibold text-white mb-2">AI Composition</h3>
            <p className="text-purple-200">
              Describe your song and AI generates melody and arrangement.
            </p>
          </div>
          <div className="p-6 bg-white/10 rounded-xl">
            <div className="text-3xl mb-4">🎶</div>
            <h3 className="text-xl font-semibold text-white mb-2">Your Performance</h3>
            <p className="text-purple-200">
              Hear your cloned voice sing your AI-created song.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Landing;