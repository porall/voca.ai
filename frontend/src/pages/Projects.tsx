import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getToken, removeToken } from '../api/auth';
import { listProjects } from '../api/projects';
import type { Project } from '../api/projects';
import Header from '../components/Header';

export default function Projects() {
    const navigate = useNavigate();
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = getToken();
        if (!token) {
            navigate('/login');
            return;
        }

        listProjects()
            .then(setProjects)
            .catch(() => {
                removeToken();
                navigate('/login');
            })
            .finally(() => setLoading(false));
    }, [navigate]);

    const getStatusLabel = (status: string) => {
        switch (status) {
            case 'completed': return '✅ 完成';
            case 'processing': return '🎵 生成中';
            case 'failed': return '❌ 失败';
            default: return '📝 草稿';
        }
    };

    const formatTime = (seconds: number | undefined) => {
        if (!seconds) return '';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900 flex items-center justify-center">
                <div className="text-white text-xl">加载中...</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-b from-purple-900 to-indigo-900">
            <Header showLogout />
            <main className="px-8 py-8">
                <div className="max-w-4xl mx-auto">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold text-white">我的创作</h2>
                        <Link to="/song-create" className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                            + 创建新歌曲
                        </Link>
                    </div>

                    {projects.length === 0 ? (
                        <div className="text-center py-12">
                            <p className="text-purple-200 mb-4">还没有创作，快去创作你的第一首AI歌曲吧！</p>
                            <Link to="/song-create" className="inline-block px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                                开始创作
                            </Link>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {projects.map(project => (
                                <div key={project.id} className="bg-white/10 p-4 rounded-lg flex items-center justify-between">
                                    <div className="flex-1">
                                        <h3 className="text-white font-medium">{project.name}</h3>
                                        <p className="text-purple-300 text-sm">
                                            {getStatusLabel(project.status)}
                                            {project.duration && ` • ${formatTime(project.duration)}`}
                                        </p>
                                        {project.error_message && (
                                            <p className="text-red-300 text-sm">{project.error_message}</p>
                                        )}
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
                                    {project.status === 'processing' && (
                                        <Link to={`/task/${project.id}`} className="px-3 py-1 bg-purple-600 text-white rounded-lg text-sm hover:bg-purple-700">
                                            查看
                                        </Link>
                                    )}
                                    {(project.status === 'draft' || project.status === 'pending') && (
                                        <Link to={`/song-create?edit=${project.id}`} className="px-3 py-1 bg-purple-600 text-white rounded-lg text-sm hover:bg-purple-700">
                                            编辑
                                        </Link>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="mt-8">
                        <Link to="/dashboard" className="text-purple-300 hover:text-white">
                            ← 返回用户中心
                        </Link>
                    </div>
                </div>
            </main>
        </div>
    );
}