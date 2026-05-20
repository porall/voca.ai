import { useState } from 'react';
import { Link } from 'react-router-dom';
import './MusicPlayer.css';

interface Song {
    id: string;
    title: string;
    duration: number;
    audioUrl: string;
    status: string;
}

const MusicPlayer = () => {
    const [songs] = useState<Song[]>([
        {
            id: '104105889',
            title: '我的夏日时光',
            duration: 183,
            audioUrl: 'https://cdn1.suno.ai/fc68734e-befa-48b6-ba64-a192876db313.mp3',
            status: 'completed',
        },
        {
            id: '104105890',
            title: '电子混音版',
            duration: 141,
            audioUrl: 'https://cdn1.suno.ai/032c94ed-340b-4ed1-99e3-0fadfec7daa2.mp3',
            status: 'completed',
        },
    ]);
    const [currentSong, setCurrentSong] = useState<Song | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);

    const formatTime = (seconds: number): string => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const togglePlay = (song: Song) => {
        if (currentSong?.id === song.id) {
            setIsPlaying(!isPlaying);
        } else {
            setCurrentSong(song);
            setIsPlaying(true);
        }
    };

    return (
        <div className="music-player-page">
            <div className="player-header">
                <h1>🎵 AI 音乐生成预览</h1>
                <Link to="/dashboard" className="back-link">← 返回用户中心</Link>
            </div>

            <div className="songs-container">
                <h2>生成的歌曲</h2>
                <div className="songs-list">
                    {songs.map((song, index) => (
                        <div
                            key={song.id}
                            className={`song-card ${currentSong?.id === song.id ? 'active' : ''}`}
                            onClick={() => togglePlay(song)}
                        >
                            <div className="song-info">
                                <span className="song-number">{index + 1}</span>
                                <div className="song-details">
                                    <h3>{song.title || `歌曲 #${song.id}`}</h3>
                                    <p>{formatTime(song.duration)}</p>
                                </div>
                            </div>
                            <button className="play-btn">
                                {currentSong?.id === song.id && isPlaying ? '⏸' : '▶'}
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            {currentSong && (
                <div className="player-footer">
                    <div className="now-playing">
                        <h3>正在播放: {currentSong.title || `#${currentSong.id}`}</h3>
                        <audio
                            src={currentSong.audioUrl}
                            autoPlay={isPlaying}
                            controls
                            onEnded={() => setIsPlaying(false)}
                            onPlay={() => setIsPlaying(true)}
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default MusicPlayer;