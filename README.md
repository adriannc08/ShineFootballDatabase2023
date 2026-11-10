# Football Data Intelligence (FDI)

Starter scaffold for a web application covering Spanish Primera and Segunda División.
Initial season: 2026-27. Historical scope: all seasons actually available through the
configured API-Football plan and endpoints.

## Important
- "All history" means all provider-supported history, not guaranteed complete player-level data.
- Verify coverage separately for squads, fixtures, lineups, appearances, player statistics and events.
- API-Football season 2026 is used as the likely provider year for 2026-27; verify this convention.
- Gemini Gems in Gemini Apps are not directly callable API resources. Files in `gemini/gems`
  are portable instruction specs; runtime integration should use Gemini API system instructions.
- "Meta-Gems" are a project-defined orchestration pattern, not an official Google feature.
- Never commit `.env` or API keys.

## Stack
FastAPI, Python, SQLAlchemy, Alembic, PostgreSQL, Next.js, API-Football,
Ollama, OpenRouter, Gemini API and OpenCode.

## Quick start
1. Copy `.env.example` to `.env` and configure credentials.
2. `docker compose up -d db`
3. `cd backend && python -m venv .venv`
4. Activate the environment and run `pip install -e ".[dev]"`
5. `uvicorn app.main:app --reload`
6. Visit `http://127.0.0.1:8000/docs`

No external API import is run automatically. First verify provider coverage and plan limits.

## Local database and web UI

Apply the starter schema to the local database after PostgreSQL is running:
`psql "postgresql://fdi:fdi_local_dev@localhost:5432/fdi" -f database/schema.sql`
Then seed the initial season:
`psql "postgresql://fdi:fdi_local_dev@localhost:5432/fdi" -f database/seed.sql`

Start the frontend:
`cd frontend && npm install && npm run dev`

The first frontend page is a visual shell only. API endpoints and data views are
subsequent implementation tasks. The SQL schema is a starter schema; production
deployment should move schema changes into reviewed Alembic migrations.
