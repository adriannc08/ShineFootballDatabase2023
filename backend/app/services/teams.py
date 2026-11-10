
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Team
from app.providers.api_football import APIFootballClient


async def sync_teams(
    session: Session,
    client: APIFootballClient,
    league_id: int,
    season: int,
) -> int:
    """
    Consulta los equipos de una competición y los guarda en PostgreSQL.
    Actualiza los equipos existentes para evitar duplicados.
    """
    payload = await client.get(
        "teams",
        {
            "league": league_id,
            "season": season,
        },
    )

    teams_data = payload.get("response", [])

    if not teams_data:
        raise ValueError("La API no ha devuelto ningún equipo.")

    saved_count = 0

    try:
        for item in teams_data:
            team_data = item.get("team", {})
            provider_id = team_data.get("id")

            if provider_id is None:
                continue

            team = session.scalar(
                select(Team).where(Team.provider_id == provider_id)
            )

            if team is None:
                team = Team(provider_id=provider_id)
                session.add(team)

            team.name = team_data.get("name") or "Unknown"
            team.country = team_data.get("country")
            team.founded = team_data.get("founded")
            team.national = bool(team_data.get("national", False))
            team.logo = team_data.get("logo")

            saved_count += 1

        session.commit()
        return saved_count

    except Exception:
        session.rollback()
        raise
