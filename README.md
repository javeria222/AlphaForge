# AlphaForge

Meeting intelligence platform with voice input, transcript analysis, and AI-powered decision extraction.

## Project Structure

- **backend/** - FastAPI backend with PostgreSQL database
  - `app/` - Application source code
  - `alembic/` - Database migrations
  - `data/` - Data storage (audio, transcripts)
  - `tests/` - Test suite

- **frontend/** - React TypeScript frontend
  - `src/` - Application source code
  - `public/` - Static assets

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure with your settings
alembic upgrade head
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`

## Features

- Voice recording and transcription
- Meeting segment analysis
- Decision extraction using AI
- Semantic search of meeting content
- RESTful API with API key authentication

## Environment Setup

Create `.env` files in both `backend/` and `frontend/` directories with required API keys:

- AssemblyAI API key (for transcription)
- OpenAI API key (for decision extraction)
- Database URL (PostgreSQL)
- API key for authentication

## Contributing

See the detailed documents in `docs/` for contributing.