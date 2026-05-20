// Task status page - shows generation progress
import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getProject, checkStatus, type Project } from '../api/projects';

export default function TaskStatusPage() {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [polling, setPolling] = useState(true);

  // Poll status every 5 seconds
  useEffect(() => {
    if (!id) {
      setError('Invalid project ID');
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        const proj = await getProject(id);
        setProject(proj);

        if (proj.status === 'completed' || proj.status === 'failed') {
          setPolling(false);
        }

        if (proj.task_id) {
          const s = await checkStatus(id!);
          
          if (s.status === 'completed' || s.status === 'failed') {
            setPolling(false);
          }
        }
      } catch (err) {
        console.error('Fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Poll every 5 seconds
    const interval = setInterval(() => {
      if (polling) {
        fetchData();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [id, polling]);

  const getStatusText = () => {
    if (!project) return '加载中...';
    
    switch (project.status) {
      case 'draft':
        return '等待生成...';
      case 'pending':
        return '任务已提交';
      case 'processing':
        return 'AI 正在创作中 🎵';
      case 'completed':
        return '🎉 完成！';
      case 'failed':
        return '❌ 生成失败';
      default:
        return '未知状态';
    }
  };

  const getStatusColor = () => {
    if (!project) return 'text-white';
    
    switch (project.status) {
      case 'draft':
      case 'pending':
        return 'text-yellow-300';
      case 'processing':
        return 'text-blue-300';
      case 'completed':
        return 'text-green-300';
      case 'failed':
        return 'text-red-300';
      default:
        return 'text-white';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-300 text-xl mb-4">{error}</div>
          <Link to="/dashboard" className="text-purple-300 hover:text-purple-200">
            返回 Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900">
      <header className="flex items-center justify-between px-8 py-4">
        <Link to="/" className="text-2xl font-bold text-white hover:opacity-80">
          🎤 Voca.ai
        </Link>
        <Link to="/dashboard" className="px-4 py-2 text-white hover:text-purple-200">
          Dashboard
        </Link>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-12">
        <div className="bg-white/10 rounded-2xl p-8">
          <h1 className="text-2xl font-bold text-white mb-2">
            {project?.name || '歌曲生成'}
          </h1>
          
          <div className={`text-xl mb-6 ${getStatusColor()}`}>
            {getStatusText()}
          </div>

          {/* Progress indicator */}
          {project?.status === 'processing' && (
            <div className="mb-6">
              <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                <div className="h-full bg-purple-500 animate-pulse w-1/2" />
              </div>
              <p className="text-purple-200 text-sm mt-2">
                AI 正在创作你的歌曲，请稍候...
              </p>
            </div>
          )}

          {/* Completed - show player */}
          {project?.status === 'completed' && project.music_url && (
            <div className="mb-6">
              <audio
                controls
                className="w-full"
                src={project.music_url}
              >
                 Your browser does not support audio.
              </audio>
              {project.duration && (
                <p className="text-purple-200 text-sm mt-2">
                  ⏱️ 时长: {Math.floor(project.duration / 60)}:{String(project.duration % 60).padStart(2, '0')}
                </p>
              )}
              {project.points_cost > 0 && (
                <p className="text-purple-200 text-sm">
                  💰 消耗积分: {project.points_cost}
                </p>
              )}
            </div>
          )}

          {/* Failed - show error */}
          {project?.status === 'failed' && (
            <div className="bg-red-500/20 border border-red-500 rounded-lg p-4 mb-6">
              <p className="text-red-200">{project.error_message || '生成失败，请重试'}</p>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-4">
            <Link
              to="/song-create"
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
            >
              🎵 创建新歌曲
            </Link>
            <Link
              to="/dashboard"
              className="px-6 py-3 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors"
            >
              📋 我的项目
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}