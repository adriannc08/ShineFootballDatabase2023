
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import Fixture, League, Team
from app.services.standings import calculate_standings
from app.services.statistics import calculate_team_statistics


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    TestingSession = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    db = TestingSession()

    league = League(
        provider_id=140,
        name="La Liga",
        country="Spain",
    )

    real_madrid = Team(
        provider_id=1,
        name="Real Madrid",
    )

    barcelona = Team(
        provider_id=2,
        name="Barcelona",
    )

    db.add_all([league, real_madrid, barcelona])
    db.flush()

    db.add_all([
        Fixture(
            provider_id=1001,
            league_id=league.id,
            home_team_id=real_madrid.id,
            away_team_id=barcelona.id,
            season=2023,
            date=datetime(2023, 8, 1, tzinfo=timezone.utc),
            status="FT",
            home_goals=2,
            away_goals=0,
        ),
        Fixture(
            provider_id=1002,
            league_id=league.id,
            home_team_id=barcelona.id,
            away_team_id=real_madrid.id,
            season=2023,
            date=datetime(2023, 8, 8, tzinfo=timezone.utc),
            status="FT",
            home_goals=1,
            away_goals=1,
        ),
    ])

    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_standings_calculation(session):
    result = calculate_standings(
        session=session,
        league_provider_id=140,
        season=2023,
    )

    assert len(result) == 2

    madrid = next(
        team for team in result
        if team["team"] == "Real Madrid"
    )

    barcelona = next(
        team for team in result
        if team["team"] == "Barcelona"
    )

    assert madrid["played"] == 2
    assert madrid["wins"] == 1
    assert madrid["draws"] == 1
    assert madrid["points"] == 4

    assert barcelona["played"] == 2
    assert barcelona["losses"] == 1
    assert barcelona["points"] == 1


def test_team_statistics(session):
    result = calculate_team_statistics(
        session=session,
        league_provider_id=140,
        season=2023,
    )

    madrid = next(
        team for team in result
        if team["team"] == "Real Madrid"
    )

    assert madrid["played"] == 2
    assert madrid["goals_for"] == 3
    assert madrid["goals_against"] == 1
    assert madrid["goal_difference"] == 2
    assert madrid["clean_sheets"] == 1
    assert madrid["points"] == 4
    assert madrid["win_percentage"] == 50.0
    assert madrid["points_per_match"] == 2.0
    assert madrid["home_wins"] == 1
    assert madrid["away_wins"] == 0
