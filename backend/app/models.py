from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Team(Base):
    __tablename__ = "teams"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    franchise_id: Mapped[int] = mapped_column(nullable=False)
    tri_code: Mapped[str] = mapped_column(nullable=False)
    current_players: Mapped[list["Player"]] = relationship("Player", back_populates="current_team")

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    headshot: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    current_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=True)
    number: Mapped[int] = mapped_column(nullable=True)
    position: Mapped[str] = mapped_column(nullable=True)
    shoots_catches: Mapped[str] = mapped_column(nullable=True)
    current_team: Mapped["Team"] = relationship("Team", back_populates="current_players")
