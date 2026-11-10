
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import League
from app.providers.api_football import APIFootballClient


async def sync_league(
    session: Session,
    client: APIFootballClient,
    league_id: int,
    season: int,
) -> League:
    payload = await client.get(
        "leagues",
        {
            "id": league_id,
            "season": season,
        },
    )

    response = payload.get("response", [])

    if not response:
        raise ValueError("La API no ha devuelto información de la competición.")

    data = response[0]
    league_data = data.get("league", {})
    country_data = data.get("country", {})

    provider_id = league_data.get("id")

    if provider_id is None:
        raise ValueError("La competición no tiene un identificador válido.")

    league = session.scalar(
        select(League).where(League.provider_id == provider_id)
    )

    try:
        if league is None:
            league = League(provider_id=provider_id)
            session.add(league)

        league.name = league_data.get("name") or "Unknown"
        league.country = country_data.get("name")
        league.logo = league_data.get("logo")

        session.commit()
        session.refresh(league)

        return league

    except Exception:
        session.rollback()
        raise
