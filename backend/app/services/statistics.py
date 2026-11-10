
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Fixture, League, Team


COMPLETED_STATUSES = {"FT", "AET", "PEN"}


def calculate_team_statistics(
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

    teams = session.scalars(
        select(Team).order_by(Team.name)
    ).all()

    stats = {}

    for team in teams:
        stats[team.id] = {
            "team_id": team.provider_id,
            "team": team.name,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "clean_sheets": 0,
            "failed_to_score": 0,
            "home_played": 0,
            "home_wins": 0,
            "away_played": 0,
            "away_wins": 0,
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

        home = stats.get(fixture.home_team_id)
        away = stats.get(fixture.away_team_id)

        if home is None or away is None:
            continue

        hg = fixture.home_goals
        ag = fixture.away_goals

        home["played"] += 1
        away["played"] += 1

        home["home_played"] += 1
        away["away_played"] += 1

        home["goals_for"] += hg
        home["goals_against"] += ag

        away["goals_for"] += ag
        away["goals_against"] += hg

        if ag == 0:
            home["clean_sheets"] += 1

        if hg == 0:
            away["clean_sheets"] += 1

        if hg == 0:
            home["failed_to_score"] += 1

        if ag == 0:
            away["failed_to_score"] += 1

        if hg > ag:
            home["wins"] += 1
            home["home_wins"] += 1
            away["losses"] += 1

        elif hg < ag:
            away["wins"] += 1
            away["away_wins"] += 1
            home["losses"] += 1

        else:
            home["draws"] += 1
            away["draws"] += 1

    results = []

    for row in stats.values():
        played = row["played"]
        row["goal_difference"] = (
            row["goals_for"] - row["goals_against"]
        )

        row["win_percentage"] = round(
            row["wins"] / played * 100, 2
        ) if played else 0.0

        row["goals_for_per_match"] = round(
            row["goals_for"] / played, 2
        ) if played else 0.0

        row["goals_against_per_match"] = round(
            row["goals_against"] / played, 2
        ) if played else 0.0

        row["points"] = row["wins"] * 3 + row["draws"]

        row["points_per_match"] = round(
            row["points"] / played, 2
        ) if played else 0.0

        row["home_win_percentage"] = round(
            row["home_wins"] / row["home_played"] * 100, 2
        ) if row["home_played"] else 0.0

        row["away_win_percentage"] = round(
            row["away_wins"] / row["away_played"] * 100, 2
        ) if row["away_played"] else 0.0

        results.append(row)

    return sorted(
        results,
        key=lambda row: (
            -row["points"],
            -row["goal_difference"],
            -row["goals_for"],
            row["team"],
        ),
    )
