
import asyncio

from app.config import settings
from app.providers.api_football import APIFootballClient


async def main():
    client = APIFootballClient(
        api_key=settings.apisports_key,
        base_url=settings.apisports_base_url,
    )

    print("Consultando API-Football...")
    print(f"Competición: 140")
    print(f"Temporada: {settings.initial_season}")

    try:
        payload = await client.get(
            "fixtures",
            {
                "league": 140,
                "season": settings.initial_season,
                "timezone": "Europe/Madrid",
            },
        )

        print("\nRespuesta recibida correctamente.")
        print("Resultados:", payload.get("results"))
        print("Paginación:", payload.get("paging"))

        fixtures = payload.get("response", [])

        print("Partidos devueltos:", len(fixtures))

        if fixtures:
            first = fixtures[0]
            print("\nPrimer partido:")
            print("ID:", first["fixture"]["id"])
            print("Fecha:", first["fixture"]["date"])
            print("Local:", first["teams"]["home"]["name"])
            print("Visitante:", first["teams"]["away"]["name"])
            print("Resultado:", first["goals"])

    except Exception as error:
        print("\nError consultando la API:")
        print(repr(error))


if __name__ == "__main__":
    asyncio.run(main())
