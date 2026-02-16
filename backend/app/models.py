from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime

class Team(Base):
    __tablename__ = "teams"
    tri_code: Mapped[str] = mapped_column(primary_key=True)
    current_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    franchise_id: Mapped[int] = mapped_column(nullable=False)
    current_players: Mapped[list["Player"]] = relationship("Player", back_populates="current_team")
    team_ids: Mapped[list[int]] = relationship("TeamHistory", back_populates="team")
    last_updated: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

class TeamHistory(Base):
    __tablename__ = "team_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    tri_code: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    team: Mapped["Team"] = relationship("Team", back_populates="team_ids")
    last_updated: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    headshot: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    current_team_tri_code: Mapped[int] = mapped_column(ForeignKey("teams.tri_code"), nullable=True)
    number: Mapped[int] = mapped_column(nullable=True)
    position: Mapped[str] = mapped_column(nullable=True)
    shoots_catches: Mapped[str] = mapped_column(nullable=True)
    current_team: Mapped["Team"] = relationship("Team", back_populates="current_players")
    last_updated: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

class SkaterGameLog(Base):
    __tablename__ = "skater_game_logs"
    # composite primary key of game_id and player_id
    game_id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), primary_key=True)
    season: Mapped[int] = mapped_column(nullable=False)
    player_team_tricode: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    opposing_team_tricode: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    game_date: Mapped[str] = mapped_column(nullable=False)
    goals: Mapped[int] = mapped_column(nullable=False)
    primary_assists: Mapped[int] = mapped_column(nullable=False)
    secondary_assists: Mapped[int] = mapped_column(nullable=False)
    points: Mapped[int] = mapped_column(nullable=False)
    x_goals: Mapped[float] = mapped_column(nullable=False)
    toi: Mapped[float] = mapped_column(nullable=False)
    high_danger_shots: Mapped[int] = mapped_column(nullable=False)
    shot_attempts: Mapped[int] = mapped_column(nullable=False)
    on_ice_x_goals_percentage: Mapped[float] = mapped_column(nullable=False)
    game_score: Mapped[float] = mapped_column(nullable=False)
    last_updated: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)