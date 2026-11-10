
import asyncio

from app.config import settings
from app.db import SessionLocal
from app.providers.api_football import APIFootballClient
from app.services.leagues import sync_league


async def main():
    client = APIFootballClient(
        api_key=settings.apisports_key,
        base_url=settings.apisports_base_url,
    )

    session = SessionLocal()

    try:
        league = await sync_league(
            session=session,
            client=client,
            league_id=140,
            season=settings.initial_season,
        )

        print("¡Competición importada correctamente!")
        print(f"Nombre: {league.name}")
        print(f"País: {league.country}")
        print(f"ID proveedor: {league.provider_id}")

    except Exception as error:
        print("Error durante la importación:")
        print(error)

    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(main())
