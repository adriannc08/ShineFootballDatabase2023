
from fastapi import FastAPI, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload
from app.services.statistics import calculate_team_statistics

from app.db import SessionLocal
from app.models import Fixture, Team
from app.services.standings import calculate_standings


app = FastAPI(
    title="Football Data Intelligence API",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health():
    return {
        "status": "ok",
        "service": "football-data-intelligence",
    }


@app.get("/api/v1/meta", tags=["system"])
def metadata():
    return {
        "initial_season": "2026-27",
        "provider": "API-Football",
        "scope": "Spain Primera and Segunda División",
        "history_policy": (
            "all provider-supported seasons; "
            "coverage must be verified"
        ),
    }


@app.get(
    "/api/v1/leagues/{league_id}/seasons/{season}/standings",
    tags=["standings"],
)
def get_standings(league_id: int, season: int):
    session = SessionLocal()

    try:
        standings = calculate_standings(
            session=session,
            league_provider_id=league_id,
            season=season,
        )

        return {
            "league_id": league_id,
            "season": season,
            "total_teams": len(standings),
            "standings": standings,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    finally:
        session.close()


@app.get("/api/v1/teams", tags=["teams"])
def get_teams():
    session = SessionLocal()

    try:
        teams = session.scalars(
            select(Team).order_by(Team.name)
        ).all()

        return {
            "total_teams": len(teams),
            "teams": [
                {
                    "id": team.id,
                    "provider_id": team.provider_id,
                    "name": team.name,
                    "country": team.country,
                    "founded": team.founded,
                    "logo": team.logo,
                }
                for team in teams
            ],
        }

    finally:
        session.close()


@app.get(
    "/api/v1/leagues/{league_id}/seasons/{season}/fixtures",
    tags=["fixtures"],
)
def get_fixtures(league_id: int, season: int):
    session = SessionLocal()

    try:
        fixtures = session.scalars(
            select(Fixture)
            .where(
                Fixture.season == season,
                Fixture.league.has(
                    provider_id=league_id
                ),
            )
            .options(
                selectinload(Fixture.home_team),
                selectinload(Fixture.away_team),
                selectinload(Fixture.league),
            )
            .order_by(Fixture.date)
        ).all()

        return {
            "league_id": league_id,
            "season": season,
            "total_fixtures": len(fixtures),
            "fixtures": [
                {
                    "id": fixture.provider_id,
                    "date": fixture.date.isoformat(),
                    "status": fixture.status,
                    "league": fixture.league.name,
                    "home_team": fixture.home_team.name,
                    "away_team": fixture.away_team.name,
                    "home_goals": fixture.home_goals,
                    "away_goals": fixture.away_goals,
                }
                for fixture in fixtures
            ],
        }

    finally:
        session.close()

@app.get(
    "/api/v1/leagues/{league_id}/seasons/{season}/statistics",
    tags=["statistics"],
)
def get_team_statistics(league_id: int, season: int):
    session = SessionLocal()

    try:
        statistics = calculate_team_statistics(
            session=session,
            league_provider_id=league_id,
            season=season,
        )

        return {
            "league_id": league_id,
            "season": season,
            "total_teams": len(statistics),
            "statistics": statistics,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    finally:
        session.close()


@app.get("/api/v1/teams/{team_id}", tags=["teams"])
def get_team_detail(
    team_id: int,
    league_id: int = 140,
    season: int = 2023,
):
    session = SessionLocal()

    try:
        team = session.scalar(
            select(Team).where(Team.provider_id == team_id)
        )

        if team is None:
            raise HTTPException(
                status_code=404,
                detail="Equipo no encontrado."
            )

        statistics = calculate_team_statistics(
            session=session,
            league_provider_id=league_id,
            season=season,
        )

        team_statistics = next(
            (
                item for item in statistics
                if item["team_id"] == team_id
            ),
            None,
        )

        fixtures = session.scalars(
            select(Fixture)
            .where(
                Fixture.season == season,
                Fixture.league.has(provider_id=league_id),
                or_(
                    Fixture.home_team_id == team.id,
                    Fixture.away_team_id == team.id,
                ),
            )
            .options(
                selectinload(Fixture.home_team),
                selectinload(Fixture.away_team),
            )
            .order_by(Fixture.date.desc())
            .limit(5)
        ).all()

        return {
            "team": {
                "id": team.provider_id,
                "name": team.name,
                "country": team.country,
                "founded": team.founded,
                "logo": team.logo,
            },
            "league_id": league_id,
            "season": season,
            "statistics": team_statistics,
            "recent_fixtures": [
                {
                    "date": fixture.date.isoformat(),
                    "status": fixture.status,
                    "home_team": fixture.home_team.name,
                    "away_team": fixture.away_team.name,
                    "home_goals": fixture.home_goals,
                    "away_goals": fixture.away_goals,
                }
                for fixture in fixtures
            ],
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    finally:
        session.close()
