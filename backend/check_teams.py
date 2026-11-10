
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Team


def main():
    session = SessionLocal()

    try:
        teams = session.scalars(
            select(Team).order_by(Team.name)
        ).all()

        print(f"\nEquipos almacenados: {len(teams)}\n")

        for team in teams:
            print(f"{team.name} | ID proveedor: {team.provider_id}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
