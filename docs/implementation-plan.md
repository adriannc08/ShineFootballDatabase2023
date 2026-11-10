# Implementation plan

## Gate 0: API-Football feasibility
Verify Spain league IDs from provider response, 2026-27 season convention,
historical coverage and endpoint coverage separately for teams, squads, fixtures,
lineups, player appearances, player statistics and events. Check plan quotas,
licensing, rate limits and retention terms before bulk import.

## Milestone 1: Data foundation
Add SQLAlchemy models, Alembic initial migration, provenance registry and idempotent
ingestion tests.

## Milestone 2: Historical import
Enumerate all provider-supported seasons. Import fixtures/results first, then squads,
lineups and player stats only where available. Make jobs resumable and rate-limited.

## Milestone 3: API and web
Implement player, team, squad, season and match endpoints; player career history;
team results and head-to-head views derived from matches.

## Milestone 4: AI
Use Ollama for local tasks, OpenRouter for selectable models and Gemini API for
structured review. LLMs must retrieve facts from the database and cannot create records.

## Milestone 5: Production
Add authentication, backups, monitoring, security review, scheduled sync and freshness dashboard.
