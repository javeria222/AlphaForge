# AlphaForge Backend

FastAPI backend for meeting intelligence and decision extraction.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.
