import asyncio

from app.config import settings
from app.providers.api_football import APIFootballClient


async def main():
    api = APIFootballClient(
        api_key=settings.apisports_key,
        base_url=settings.apisports_base_url,
    )

    try:
        result = await api.get(
            "teams",
            {
                "league": 140,
                "season": settings.initial_season,
            },
        )

        teams = result.get("response", [])

        print(f"Equipos encontrados: {len(teams)}")

        for item in teams:
            team = item["team"]
            print(f"- {team['name']} (ID: {team['id']})")

    except Exception as error:
        print("Error al consultar los equipos:")
        print(error)


if __name__ == "__main__":
    asyncio.run(main())