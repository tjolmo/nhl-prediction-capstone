from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
import datetime

class Team(Base):
    __tablename__ = "teams"
    tri_code: Mapped[str] = mapped_column(primary_key=True)
    current_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    franchise_id: Mapped[int] = mapped_column(nullable=False)
    current_players: Mapped[list["Player"]] = relationship("Player", back_populates="current_team")
    team_ids: Mapped[list[int]] = relationship("TeamHistory", back_populates="team")
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    roster_last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

class TeamHistory(Base):
    __tablename__ = "team_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    tri_code: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    team: Mapped["Team"] = relationship("Team", back_populates="team_ids")
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

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
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    game_logs: Mapped[list["SkaterGameLog"]] = relationship("SkaterGameLog", back_populates="player")
    goalie_game_logs: Mapped[list["GoalieGameLog"]] = relationship("GoalieGameLog", back_populates="player")
    game_log_last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

class SkaterGameLog(Base):
    __tablename__ = "skater_game_logs"
    # composite primary key of game_id and player_id
    game_id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    season: Mapped[int] = mapped_column(nullable=False)
    home_away: Mapped[str] = mapped_column(nullable=True)
    player_team_tricode: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    opposing_team_tricode: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    game_date: Mapped[int] = mapped_column(nullable=False)
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
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    player: Mapped["Player"] = relationship("Player", back_populates="game_logs")

class GoalieGameLog(Base):
    __tablename__ = "goalie_game_logs"
    # composite primary key of game_id and player_id
    game_id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    season: Mapped[int] = mapped_column(nullable=False)
    home_away: Mapped[str] = mapped_column(nullable=True)
    player_team_tricode: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    opposing_team_tricode: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    game_date: Mapped[int] = mapped_column(nullable=False)
    toi: Mapped[float] = mapped_column(nullable=False)
    x_goals_against: Mapped[float] = mapped_column(nullable=False)
    goals_against: Mapped[int] = mapped_column(nullable=False)
    unblocked_shot_attempts: Mapped[int] = mapped_column(nullable=False)
    x_rebounds: Mapped[float] = mapped_column(nullable=False)
    rebounds: Mapped[int] = mapped_column(nullable=False)
    x_freeze: Mapped[float] = mapped_column(nullable=False)
    freeze: Mapped[int] = mapped_column(nullable=False)
    x_sog: Mapped[float] = mapped_column(nullable=False)
    sog: Mapped[int] = mapped_column(nullable=False)
    x_play_stopped: Mapped[float] = mapped_column(nullable=False)
    play_stopped: Mapped[int] = mapped_column(nullable=False)
    x_play_continued_in_zone: Mapped[float] = mapped_column(nullable=False)
    x_play_continued_outside_zone: Mapped[float] = mapped_column(nullable=False)
    flurry_adjusted_x_goals: Mapped[float] = mapped_column(nullable=False)
    low_danger_shots: Mapped[int] = mapped_column(nullable=False)
    medium_danger_shots: Mapped[int] = mapped_column(nullable=False)
    high_danger_shots: Mapped[int] = mapped_column(nullable=False)
    low_danger_x_goals: Mapped[float] = mapped_column(nullable=False)
    medium_danger_x_goals: Mapped[float] = mapped_column(nullable=False)
    high_danger_x_goals: Mapped[float] = mapped_column(nullable=False)
    blocked_shot_attempts: Mapped[int] = mapped_column(nullable=False)
    penality_minutes: Mapped[int] = mapped_column(nullable=False)
    penalties: Mapped[int] = mapped_column(nullable=False)
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    player: Mapped["Player"] = relationship("Player", back_populates="goalie_game_logs")

class Games(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    home_team_tri_code: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    away_team_tri_code: Mapped[str] = mapped_column(ForeignKey("teams.tri_code"), nullable=False)
    season: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[int] = mapped_column(nullable=False)
    venue: Mapped[str] = mapped_column(nullable=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    home_team_logo: Mapped[str] = mapped_column(nullable=True)
    away_team_logo: Mapped[str] = mapped_column(nullable=True)
    home_score: Mapped[int] = mapped_column(nullable=True)
    away_score: Mapped[int] = mapped_column(nullable=True)
    game_state: Mapped[str] = mapped_column(nullable=False)
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))