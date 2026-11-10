
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Fixture, League, Team


COMPLETED_STATUSES = {"FT", "AET", "PEN"}


def calculate_standings(
    session: Session,
    league_provider_id: int,
    season: int,
) -> list[dict]:
    league = session.scalar(
        select(League).where(
            League.provider_id == league_provider_id
        )
    )

    if league is None:
        raise ValueError("La competición no está guardada.")

    teams = session.scalars(select(Team)).all()

    standings = {}

    for team in teams:
        standings[team.id] = {
            "team": team.name,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }

    fixtures = session.scalars(
        select(Fixture).where(
            Fixture.league_id == league.id,
            Fixture.season == season,
            Fixture.status.in_(COMPLETED_STATUSES),
        )
    ).all()

    for fixture in fixtures:
        if (
            fixture.home_goals is None
            or fixture.away_goals is None
        ):
            continue

        home = standings.get(fixture.home_team_id)
        away = standings.get(fixture.away_team_id)

        if home is None or away is None:
            continue

        home_goals = fixture.home_goals
        away_goals = fixture.away_goals

        home["played"] += 1
        away["played"] += 1

        home["goals_for"] += home_goals
        home["goals_against"] += away_goals

        away["goals_for"] += away_goals
        away["goals_against"] += home_goals

        if home_goals > away_goals:
            home["wins"] += 1
            home["points"] += 3
            away["losses"] += 1

        elif home_goals < away_goals:
            away["wins"] += 1
            away["points"] += 3
            home["losses"] += 1

        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    for row in standings.values():
        row["goal_difference"] = (
            row["goals_for"] - row["goals_against"]
        )

    return sorted(
        standings.values(),
        key=lambda row: (
            -row["points"],
            -row["goal_difference"],
            -row["goals_for"],
            row["team"],
        ),
    )
