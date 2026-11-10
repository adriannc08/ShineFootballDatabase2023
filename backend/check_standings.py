
from app.db import SessionLocal
from app.services.standings import calculate_standings


def main():
    session = SessionLocal()

    try:
        standings = calculate_standings(
            session=session,
            league_provider_id=140,
            season=2023,
        )

        print("\nCLASIFICACIÓN DE LALIGA 2023-24")
        print("=" * 90)

        print(
            f"{'POS':<5}"
            f"{'EQUIPO':<23}"
            f"{'PJ':>4}"
            f"{'PG':>4}"
            f"{'PE':>4}"
            f"{'PP':>4}"
            f"{'GF':>5}"
            f"{'GC':>5}"
            f"{'DG':>5}"
            f"{'PTS':>5}"
        )

        print("-" * 90)

        for position, team in enumerate(standings, start=1):
            print(
                f"{position:<5}"
                f"{team['team']:<23}"
                f"{team['played']:>4}"
                f"{team['wins']:>4}"
                f"{team['draws']:>4}"
                f"{team['losses']:>4}"
                f"{team['goals_for']:>5}"
                f"{team['goals_against']:>5}"
                f"{team['goal_difference']:>5}"
                f"{team['points']:>5}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()
