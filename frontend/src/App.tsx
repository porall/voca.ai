import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Landing from './Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import VoiceUpload from './pages/VoiceUpload'
import MusicPlayer from './pages/MusicPlayer'
import SongCreate from './pages/SongCreate'
import TaskStatus from './pages/TaskStatus'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/voice-upload" element={<VoiceUpload />} />
        <Route path="/music-player" element={<MusicPlayer />} />
        <Route path="/song-create" element={<SongCreate />} />
        <Route path="/task/:id" element={<TaskStatus />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}