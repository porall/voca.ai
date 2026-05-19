# Voca.ai

> Your Voice, Your Song

AI-powered music creation platform - generate songs with your own cloned voice.

## Tech Stack

- **Frontend**: React 18 + TypeScript + Vite + Tailwind
- **Backend**: FastAPI + PostgreSQL + Celery
- **AI**: Suno (music) + Reecho (voice cloning)

## Getting Started

```bash
# Install dependencies
npm install

# Run frontend
npm run dev

# Run backend (requires Python 3.10+)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Development

Follow TDD methodology:
1. Write failing test first
2. Write minimal code to pass
3. Refactor

```bash
# Run tests
pytest tests/ -q
```

## License

MIT