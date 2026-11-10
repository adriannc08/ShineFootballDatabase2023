import asyncio

from app.config import settings
from app.providers.api_football import APIFootballClient


async def main():
    api = APIFootballClient(
        api_key=settings.apisports_key,
        base_url=settings.apisports_base_url,
    )

    try:
        result = await api.get("status", {})
        print("¡Conexión correcta con API-Football!")
        print("Respuesta recibida correctamente.")
        print(result)
    except Exception as error:
        print("Error al conectar con API-Football:")
        print(error)


if __name__ == "__main__":
    asyncio.run(main())