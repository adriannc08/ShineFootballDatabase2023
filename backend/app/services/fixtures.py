
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Fixture, League, Team
from app.providers.api_football import APIFootballClient


async def sync_fixtures(
    session: Session,
    client: APIFootballClient,
    league_provider_id: int,
    season: int,
) -> int:
    league = session.scalar(
        select(League).where(
            League.provider_id == league_provider_id
        )
    )

    if league is None:
        raise ValueError(
            "La competición no está guardada. "
            "Ejecuta primero import_league.py."
        )

    teams = session.scalars(select(Team)).all()
    team_ids = {
        team.provider_id: team.id
        for team in teams
    }

    payload = await client.get(
        "fixtures",
        {
            "league": league_provider_id,
            "season": season,
            "timezone": "Europe/Madrid",
        },
    )

    fixtures_data = payload.get("response", [])

    if not fixtures_data:
        raise ValueError(
            "La API no ha devuelto partidos para esta competición y temporada."
        )

    total_saved = 0

    try:
        for item in fixtures_data:
            fixture_data = item.get("fixture", {})
            league_data = item.get("league", {})
            teams_data = item.get("teams", {})
            goals_data = item.get("goals", {})

            provider_id = fixture_data.get("id")

            home_provider_id = teams_data.get(
                "home", {}
            ).get("id")

            away_provider_id = teams_data.get(
                "away", {}
            ).get("id")

            if provider_id is None:
                continue

            home_id = team_ids.get(home_provider_id)
            away_id = team_ids.get(away_provider_id)

            if home_id is None or away_id is None:
                raise ValueError(
                    f"Faltan equipos importados en el partido {provider_id}."
                )

            if league_data.get("id") != league_provider_id:
                raise ValueError(
                    f"Competición inesperada en el partido {provider_id}."
                )

            date_text = fixture_data.get("date")

            if not date_text:
                raise ValueError(
                    f"El partido {provider_id} no tiene fecha."
                )

            match_date = datetime.fromisoformat(
                date_text.replace("Z", "+00:00")
            )

            status = fixture_data.get(
                "status", {}
            ).get("short", "UNK")

            fixture = session.scalar(
                select(Fixture).where(
                    Fixture.provider_id == provider_id
                )
            )

            if fixture is None:
                fixture = Fixture(provider_id=provider_id)
                session.add(fixture)

            fixture.league_id = league.id
            fixture.home_team_id = home_id
            fixture.away_team_id = away_id
            fixture.season = season
            fixture.date = match_date
            fixture.status = status
            fixture.home_goals = goals_data.get("home")
            fixture.away_goals = goals_data.get("away")

            total_saved += 1

        session.commit()
        return total_saved

    except Exception:
        session.rollback()
        raise
