
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    logo: Mapped[str | None] = mapped_column(String(500), nullable=True)


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    founded: Mapped[int | None] = mapped_column(Integer, nullable=True)
    national: Mapped[bool] = mapped_column(Boolean, default=False)
    logo: Mapped[str | None] = mapped_column(String(500), nullable=True)


class Fixture(Base):
    __tablename__ = "fixtures"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(unique=True, index=True)

    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id"))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    season: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(30))

    home_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)

    league: Mapped["League"] = relationship()
    home_team: Mapped["Team"] = relationship(foreign_keys=[home_team_id])
    away_team: Mapped["Team"] = relationship(foreign_keys=[away_team_id])

class CustomCompetition(Base):
    __tablename__ = "custom_competitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=sa.func.now(),
    )


class CustomSeason(Base):
    __tablename__ = "custom_seasons"
    __table_args__ = (
        UniqueConstraint("competition_id", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_id: Mapped[int] = mapped_column(
        ForeignKey("custom_competitions.id")
    )
    name: Mapped[str] = mapped_column(String(80))
    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_hypothetical: Mapped[bool] = mapped_column(Boolean, default=False)


class CustomTeam(Base):
    __tablename__ = "custom_teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    short_name: Mapped[str | None] = mapped_column(String(30), nullable=True)
    logo: Mapped[str | None] = mapped_column(String(500), nullable=True)


class CustomSeasonTeam(Base):
    __tablename__ = "custom_season_teams"
    __table_args__ = (
        UniqueConstraint("season_id", "team_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("custom_seasons.id")
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("custom_teams.id")
    )


class CustomFixture(Base):
    __tablename__ = "custom_fixtures"
    __table_args__ = (
        CheckConstraint("home_team_id != away_team_id"),
        CheckConstraint("home_goals IS NULL OR home_goals >= 0"),
        CheckConstraint("away_goals IS NULL OR away_goals >= 0"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("custom_seasons.id")
    )
    matchday: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("custom_teams.id")
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("custom_teams.id")
    )
    home_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default="scheduled"
    )
