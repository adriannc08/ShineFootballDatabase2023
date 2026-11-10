
from sqlalchemy import func, select

from app.db import SessionLocal
from app.models import Fixture, League, Team


def main():
    session = SessionLocal()

    try:
        total = session.scalar(
            select(func.count()).select_from(Fixture)
        )

        print(f"\nTotal de partidos almacenados: {total}\n")

        fixtures = session.scalars(
            select(Fixture)
            .order_by(Fixture.date)
            .limit(10)
        ).all()

        for match in fixtures:
            home = session.get(Team, match.home_team_id)
            away = session.get(Team, match.away_team_id)
            league = session.get(League, match.league_id)

            score = (
                f"{match.home_goals} - {match.away_goals}"
                if match.home_goals is not None
                and match.away_goals is not None
                else "Sin resultado"
            )

            print(f"Competición: {league.name}")
            print(f"Partido: {home.name} vs {away.name}")
            print(f"Fecha: {match.date}")
            print(f"Resultado: {score}")
            print(f"Estado: {match.status}")
            print("-" * 45)

    finally:
        session.close()


if __name__ == "__main__":
    main()
