
import asyncio

from app.config import settings
from app.db import SessionLocal
from app.providers.api_football import APIFootballClient
from app.services.fixtures import sync_fixtures


async def main():
    client = APIFootballClient(
        api_key=settings.apisports_key,
        base_url=settings.apisports_base_url,
    )

    session = SessionLocal()

    try:
        count = await sync_fixtures(
            session=session,
            client=client,
            league_provider_id=140,
            season=settings.initial_season,
        )

        print("¡Importación de partidos completada!")
        print(f"Partidos guardados o actualizados: {count}")

    except Exception as error:
        print("Error durante la importación:")
        print(error)

    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(main())
