import { useState, useEffect, useRef } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getProject } from '../api/projects';
import type { Project } from '../api/projects';
import './MusicPlayer.css';

const MusicPlayer = () => {
    const [searchParams] = useSearchParams();
    const projectId = searchParams.get('id');
    
    const [project, setProject] = useState<Project | null>(null);
    const [loading, setLoading] = useState(!!projectId);
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef<HTMLAudioElement>(null);

    useEffect(() => {
        if (projectId) {
            getProject(projectId)
                .then(p => {
                    setProject(p);
                    if (p.status !== 'completed') {
                        console.warn('Project not completed');
                    }
                })
                .catch(err => console.error('Failed to load project:', err))
                .finally(() => setLoading(false));
        }
    }, [projectId]);

    useEffect(() => {
        return () => {
            if (audioRef.current) {
                audioRef.current.pause();
            }
        };
    }, []);

    const formatTime = (seconds: number | undefined): string => {
        if (!seconds) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const togglePlay = () => {
        if (!audioRef.current || !project?.music_url) return;
        
        if (isPlaying) {
            audioRef.current.pause();
        } else {
            audioRef.current.play().catch(console.error);
        }
    };

    if (loading) {
        return (
            <div className="music-player-page">
                <div className="player-header">
                    <h1>🎵 音乐预览</h1>
                    <Link to="/dashboard" className="back-link">← 返回用户中心</Link>
                </div>
                <div className="loading">加载中...</div>
            </div>
        );
    }

    if (!project) {
        return (
            <div className="music-player-page">
                <div className="player-header">
                    <h1>🎵 音乐预览</h1>
                    <Link to="/dashboard" className="back-link">← 返回用户中心</Link>
                </div>
                <div className="error">
                    <p>请选择一首歌曲</p>
                    <Link to="/dashboard" className="btn">前往用户中心</Link>
                </div>
            </div>
        );
    }

    if (project.status !== 'completed') {
        return (
            <div className="music-player-page">
                <div className="player-header">
                    <h1>🎵 音乐预览</h1>
                    <Link to="/dashboard" className="back-link">← 返回用户中心</Link>
                </div>
                <div className="error">
                    <p>歌曲还在生成中，请稍后再试</p>
                    <Link to={`/task/${project.id}`} className="btn">查看进度</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="music-player-page">
            <div className="player-header">
                <h1>🎵 音乐预览</h1>
                <div className="flex gap-3">
                    {project.music_url && (
                        <a
                            href={project.music_url}
                            download={project.name + '.mp3'}
                            className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                        >
                            ⬇️ 下载
                        </a>
                    )}
                    <Link to="/dashboard" className="back-link">← 返回用户中心</Link>
                </div>
            </div>

            <div className="player-main">
                <div className="album-art">
                    {project.cover_url ? (
                        <img src={project.cover_url} alt={project.name} />
                    ) : (
                        <div className="album-placeholder">🎵</div>
                    )}
                </div>

                <div className="song-info-section">
                    <h2>{project.name}</h2>
                    {project.suno_title && (
                        <p className="suno-title">原曲: {project.suno_title}</p>
                    )}
                    <p className="duration">{formatTime(project.duration)}</p>
                </div>

                <div className="player-controls">
                    <button onClick={togglePlay} className="play-btn-large">
                        {isPlaying ? '⏸' : '▶'}
                    </button>
                </div>

                {project.music_url && (
                    <audio
                        ref={audioRef}
                        src={project.music_url}
                        onPlay={() => setIsPlaying(true)}
                        onPause={() => setIsPlaying(false)}
                        onEnded={() => setIsPlaying(false)}
                    />
                )}
            </div>

            <div className="player-footer">
                <Link to="/dashboard" className="btn">返回用户中心</Link>
            </div>
        </div>
    );
};

export default MusicPlayer;