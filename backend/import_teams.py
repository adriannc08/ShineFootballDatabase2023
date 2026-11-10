
import asyncio

from app.config import settings
from app.db import SessionLocal
from app.providers.api_football import APIFootballClient
from app.services.teams import sync_teams


async def main():
    client = APIFootballClient(
        api_key=settings.apisports_key,
        base_url=settings.apisports_base_url,
    )

    session = SessionLocal()

    try:
        count = await sync_teams(
            session=session,
            client=client,
            league_id=140,
            season=settings.initial_season,
        )

        print(f"¡Importación completada! Equipos guardados o actualizados: {count}")

    except Exception as error:
        print("Ha ocurrido un error durante la importación:")
        print(error)

    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(main())
