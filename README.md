# Voca.ai

> 你的声音，你的歌

AI 音乐创作平台 — 用你自己的声音克隆演唱 AI 生成的歌曲。

## 功能特性

- 🎤 **声音克隆** — 上传你的演唱录音，AI 会克隆你的声音
- 🎵 **AI 音乐生成** — 输入歌词和风格，AI 自动生成配乐
- 🎶 **智能翻唱** — 用克隆声音演唱生成的歌曲
- 👤 **用户系统** — 注册、登录、管理自己的声音和作品

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18 + TypeScript + Vite + Tailwind |
| 后端 | FastAPI + SQLite（开发）/ PostgreSQL（生产） |
| AI | Suno（音乐生成）+ Reecho（声音克隆） |
| 部署 | Docker + ngrok |

## 快速开始

```bash
# 安装前端依赖
cd frontend
npm install

# 启动前端开发服务器
npm run dev

# 启动后端（需要 Python 3.10+）
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录，获取 JWT token |
| GET | `/api/auth/me` | 获取当前用户信息 |
| GET | `/api/voices` | 列出已克隆的声音 |
| POST | `/api/voices/upload` | 上传音频文件克隆声音 |
| DELETE | `/api/voices/{id}` | 删除声音 |
| GET | `/api/projects` | 列出音乐项目 |
| POST | `/api/projects` | 创建新项目 |

## 开发规范

采用 TDD（测试驱动开发）方式：

1. 先写测试描述需求
2. 运行测试确认失败
3. 写代码让测试通过
4. 重构优化

```bash
# 运行后端测试
cd backend
pytest tests/ -v

# 运行前端构建
cd frontend
npm run build
```

## 项目结构

```
voca.ai/
├── frontend/           # React 前端
│   └── src/
│       ├── pages/      # 页面组件
│       ├── api/       # API 客户端
│       └── App.tsx    # 路由配置
├── backend/            # FastAPI 后端
│   └── app/
│       ├── api/       # API 路由
│       ├── services/   # 业务逻辑
│       └── models/    # 数据模型
└── README.md
```

## 许可证

MIT