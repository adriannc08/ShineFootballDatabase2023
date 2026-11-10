import os
import sys
import httpx

BASE = os.getenv("APISPORTS_BASE_URL", "https://v3.football.api-sports.io").rstrip("/")
KEY = os.getenv("APISPORTS_KEY", "")
SEASON = os.getenv("INITIAL_SEASON", "2026")

def main() -> int:
    if not KEY:
        print("ERROR: configura APISPORTS_KEY en tu entorno.")
        return 2
    response = httpx.get(
        f"{BASE}/leagues",
        params={"country": "Spain", "season": SEASON},
        headers={"x-apisports-key": KEY},
        timeout=30.0,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        print("API-Football errors:", payload["errors"])
        return 1

    print(f"Competiciones devueltas para Spain / season={SEASON}:")
    for item in payload.get("response", []):
        league = item.get("league", {})
        country = item.get("country", {})
        coverage = item.get("seasons", [])
        season_info = next((s for s in coverage if str(s.get("year")) == str(SEASON)), {})
        cov = season_info.get("coverage", {})
        fixtures = cov.get("fixtures", {})
        print({
            "league_id": league.get("id"),
            "name": league.get("name"),
            "country": country.get("name"),
            "season": SEASON,
            "players": cov.get("players"),
            "fixtures": fixtures,
            "standings": cov.get("standings"),
        })
    print("\nRevisa los nombres/IDs y la cobertura por competición antes de importar.")
    print("La cobertura True no garantiza que todos los registros estén completos.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
