// Create new song page with presets
import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getToken, getStoredUser, type User } from '../api/auth';
import { listVoices, type Voice } from '../api/voices';
import { createProject, generateMusic } from '../api/projects';
import './SongCreate.css';

// Preset styles - artist presets fill description
const ARTIST_PRESETS = [
  { id: 'jjlin', name: '林俊杰', tags: 'pop, r&b, ballad', desc: '一首R&B节奏的抒情歌曲，温暖深情的声线，转音运用自如，表达都市爱情故事的甜蜜与忧伤，JJ式细腻情感表达' },
  { id: 'jaychou', name: '周杰伦', tags: 'pop, hip-hop, chinese-rock', desc: '中国风嘻哈流行，周杰伦式饶舌与抒情结合，方文山词风意境，周氏经典钢琴前奏，副歌旋律性强' },
  { id: 'jolin', name: '蔡依林', tags: 'pop, electronic, dance', desc: 'EDM舞曲风格，强劲电子节拍，节奏感强烈，舞曲元素丰富，适合舞池/健身房场景' },
  { id: 'eason', name: '陈奕迅', tags: 'pop, ballad, cantonese', desc: '深情粤语抒情歌，Eason式沙哑声线，感情层次丰富，表达孤独、深情或释然，叙事感强' },
  { id: 'a_mei', name: '张惠妹', tags: 'pop, rock, ballad', desc: '张力十足的抒情摇滚，副歌爆发力强，表达浓烈情感，A-Mei式深情呐喊与柔情并存' },
  { id: 'joker_xue', name: '薛之谦', tags: 'pop, ballad', desc: '薛氏情歌风格，都市情感叙事，字字戳心的歌词旋律，微醺般的诗意抒情，治愈系都市情歌' },
  { id: 'taylor', name: 'Taylor Swift', tags: 'pop, country-pop', desc: 'Taylor Swift式流行乡村，打动人心的歌词叙事，旋律朗朗上口，流行度极高的现代流行抒情' },
  { id: 'ed', name: 'Ed Sheeran', tags: 'pop, acoustic, folk', desc: 'Acoustic民谣风格，吉他弹唱，Ed Sheeran式简单却深刻的情感表达，清新温柔的旋律' },
];

// Genre presets add to tags (can combine with artist)
const GENRE_PRESETS = [
  { id: 'pop', name: '流行', tags: 'pop', desc: '主流流行' },
  { id: 'rock', name: '摇滚', tags: 'rock', desc: '摇滚' },
  { id: 'electronic', name: '电子', tags: 'electronic', desc: '电子' },
  { id: 'ballad', name: '抒情', tags: 'ballad', desc: '抒情' },
  { id: 'hiphop', name: '嘻哈', tags: 'hip-hop', desc: '嘻哈' },
  { id: 'jazz', name: '爵士', tags: 'jazz', desc: '爵士' },
  { id: 'classical', name: '古典', tags: 'classical', desc: '古典' },
  { id: 'folk', name: '民谣', tags: 'folk', desc: '民谣' },
];

const DURATION_OPTIONS = [
  { value: 120, label: '2分钟' },
  { value: 180, label: '3分钟' },
  { value: 240, label: '4分钟' },
];

const MODEL_OPTIONS = [
  { value: 'chirp-fenix', label: 'Fenix (最新)' },
  { value: 'chirp-v4', label: 'V4' },
  { value: 'chirp-v3-5', label: 'V3.5' },
];

export default function SongCreate() {
  const [user, setUser] = useState<User | null>(null);
  const [voices, setVoices] = useState<Voice[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  
  const navigate = useNavigate();
  
  // Form fields
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [tags, setTags] = useState('');
  const [duration, setDuration] = useState(180);
  const [isInstrumental, setIsInstrumental] = useState(false);
  const [customMode, setCustomMode] = useState(false);
  const [lyrics, setLyrics] = useState('');
  const [selectedVoiceId, setSelectedVoiceId] = useState('');
  const [selectedArtist, setSelectedArtist] = useState('');
  const [model, setModel] = useState('chirp-fenix');
  
  // Show advanced options
  const [showAdvanced, setShowAdvanced] = useState(false);

  useEffect(() => {
    const storedUser = getStoredUser();
    if (storedUser) {
      setUser(storedUser);
    }
    listVoices().then(setVoices).catch(console.error);
    setLoading(false);
  }, []);

  // Apply artist preset - fills the description (replaces)
  const applyArtistPreset = (preset: typeof ARTIST_PRESETS[0]) => {
    setDesc(preset.desc);
    setSelectedArtist(preset.id);
  };
  
  // Apply genre preset - adds to tags (can combine with artist)
  const applyGenrePreset = (preset: typeof GENRE_PRESETS[0]) => {
    const currentTags = tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : [];
    const newTags = preset.tags.split(',').map(t => t.trim());
    const merged = [...new Set([...currentTags, ...newTags])].join(', ');
    setTags(merged);
  };

  // Build description with duration hint
  const buildDescription = (): string => {
    let result = desc;
    if (duration !== 180) {
      const mins = duration / 60;
      result = `一首${mins}分钟的${result}`;
    }
    return result;
  };

const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    
    try {
      const token = getToken();
      if (!token) {
        navigate('/login');
        return;
      }
      
      const payload = {
        name: title,
        gpt_description: buildDescription(),
        music_genre: tags,
        make_instrumental: isInstrumental,
        style: selectedArtist,
        ...(customMode && lyrics && { lyrics }),
        mv: model,
        ...(selectedVoiceId && { voice_id: selectedVoiceId }),
      };
      
      console.log('Creating project:', payload);
      
      // Create project first
      const project = await createProject(payload);
      console.log('Project created:', project.id);
      
      // Then generate music
      const result = await generateMusic(project.id);
      console.log('Generation started:', result);
      
      setSuccess(true);
      // Navigate to task status page
      setTimeout(() => navigate(`/task/${project.id}`), 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成失败');
    } finally {
      setSubmitting(false);
    }
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
      <header className="flex items-center justify-between px-8 py-4">
        <Link to="/" className="text-2xl font-bold text-white hover:opacity-80">🎤 Voca.ai</Link>
        {user ? (
          <nav className="flex gap-4 items-center">
            <span className="text-purple-200">Welcome, {user.nickname || user.email}</span>
            <Link to="/dashboard" className="px-4 py-2 text-white hover:text-purple-200">Dashboard</Link>
          </nav>
        ) : (
          <nav className="flex gap-4">
            <Link to="/login" className="px-4 py-2 text-white hover:text-purple-200">Login</Link>
          </nav>
        )}
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white text-center mb-2">🎵 创建新歌曲</h1>
        <p className="text-purple-200 text-center mb-8">描述你想要的歌曲，AI 帮你创作</p>

        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-200 p-3 rounded-lg mb-4">{error}</div>
        )}
        
        {success && (
          <div className="bg-green-500/20 border border-green-500 text-green-200 p-3 rounded-lg mb-4">✅ 歌曲创建成功！正在跳转...</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <label className="block text-purple-200 mb-2">歌曲标题 *</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-purple-500/30 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-500"
              placeholder="给你的歌曲起个名字"
              required
            />
          </div>

          {/* Artist Presets */}
          <div>
            <label className="block text-purple-200 mb-2">🎤 歌手风格（填描述）</label>
            <div className="flex flex-wrap gap-2">
              {ARTIST_PRESETS.map((preset) => (
                <button
                  key={preset.id}
                  type="button"
                  onClick={() => applyArtistPreset(preset)}
                  className="px-3 py-2 bg-white/10 hover:bg-purple-600 text-white text-sm rounded-lg transition-colors"
                >
                  {preset.name}
                </button>
              ))}
            </div>
          </div>

          {/* Genre Presets */}
          <div>
            <label className="block text-purple-200 mb-2">🎶 风格类型（加标签，可多选）</label>
            <div className="flex flex-wrap gap-2">
              {GENRE_PRESETS.map((preset) => (
                <button
                  key={preset.id}
                  type="button"
                  onClick={() => applyGenrePreset(preset)}
                  className="px-3 py-2 bg-white/10 hover:bg-pink-600 text-white text-sm rounded-lg transition-colors"
                >
                  {preset.name}
                </button>
              ))}
            </div>
          </div>

          {/* Music Description */}
          <div>
            <label className="block text-purple-200 mb-2">音乐描述 *</label>
            <textarea
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-purple-500/30 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-500 h-24 resize-none"
              placeholder="描述你想要的歌曲：风格、情绪、场景... 例如：一首关于夏天的欢快流行歌"
              required
            />
          </div>

          {/* Style Tags */}
          <div>
            <label className="block text-purple-200 mb-2">风格标签（可手动编辑）</label>
            <input
              type="text"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-purple-500/30 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-500"
              placeholder="pop, rock, ballad"
            />
          </div>

          {/* Duration */}
          <div>
            <label className="block text-purple-200 mb-2">歌曲时长（AI 会尽量按此生成，最终2-4分钟）</label>
            <div className="flex gap-2">
              {DURATION_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  onClick={() => setDuration(opt.value)}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    duration === opt.value ? 'bg-purple-600 text-white' : 'bg-white/10 text-purple-200 hover:bg-white/20'
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Mode Toggle */}
          <div className="flex gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={isInstrumental}
                onChange={(e) => setIsInstrumental(e.target.checked)}
                className="w-5 h-5 rounded border-purple-500 text-purple-600"
              />
              <span className="text-purple-200">纯音乐 (无人声)</span>
            </label>
            
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={customMode}
                onChange={(e) => setCustomMode(e.target.checked)}
                className="w-5 h-5 rounded border-purple-500 text-purple-600"
              />
              <span className="text-purple-200">自定义歌词</span>
            </label>
          </div>

          {/* Custom Lyrics */}
          {customMode && (
            <div>
              <label className="block text-purple-200 mb-2">歌词内容</label>
              <textarea
                value={lyrics}
                onChange={(e) => setLyrics(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 border border-purple-500/30 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-500 h-32 resize-none"
                placeholder="输入完整的歌词（每行一句）"
              />
            </div>
          )}

          {/* Voice Selection */}
          {!isInstrumental && voices.length > 0 && (
            <div>
              <label className="block text-purple-200 mb-2">🎙️ 选择你的声音（翻唱用）</label>
              <select
                value={selectedVoiceId}
                onChange={(e) => setSelectedVoiceId(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 border border-purple-500/30 rounded-lg text-white"
              >
                <option value="" className="text-purple-900">不使用（生成原声）</option>
                {voices.map((voice) => (
                  <option key={voice.id} value={voice.id} className="text-purple-900">{voice.name}</option>
                ))}
              </select>
            </div>
          )}

          {/* Advanced Options Toggle */}
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-purple-300 hover:text-white text-sm"
          >
            {showAdvanced ? '▼ 收起高级选项' : '▶ 显示高级选项'}
          </button>

          {/* Advanced Options */}
          {showAdvanced && (
            <div className="p-4 bg-white/5 rounded-lg space-y-4">
              <div>
                <label className="block text-purple-200 mb-2">AI 模型</label>
                <div className="flex gap-2">
                  {MODEL_OPTIONS.map((opt) => (
                    <button
                      key={opt.value}
                      type="button"
                      onClick={() => setModel(opt.value)}
                      className={`px-4 py-2 rounded-lg transition-colors ${
                        model === opt.value ? 'bg-purple-600 text-white' : 'bg-white/10 text-purple-200 hover:bg-white/20'
                      }`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={submitting}
            className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-lg font-semibold rounded-lg hover:scale-[1.02] transition-transform disabled:opacity-50"
          >
            {submitting ? '🎵 生成中...' : '🎵 生成歌曲'}
          </button>

          <p className="text-center text-purple-300 text-sm">每次生成消耗 5-10 积分</p>
        </form>
      </main>
    </div>
  );
}