from typing import Any
import httpx

class APIFootballClient:
    # Transport adapter. Keep endpoint mapping and normalization in service modules.
    def __init__(self, api_key: str, base_url: str, timeout: float = 20.0):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("APISPORTS_KEY is not configured")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/{endpoint.lstrip('/')}",
                headers={"x-apisports-key": self.api_key},
                params=params,
            )
            response.raise_for_status()
            payload = response.json()
        if payload.get("errors"):
            raise RuntimeError(f"API-Football errors: {payload['errors']}")
        return payload
