import datetime

from pydantic import BaseModel

class Last5GameInfoOut(BaseModel):
    """Output model for a team's last 5 games info"""
    game_id: int
    date: int
    home_team_tri_code: str
    away_team_tri_code: str
    home_score: int | None
    away_score: int | None

    class Config:
        from_attributes = True

class TeamBasicInfoOut(BaseModel):
    """Output model for a team's basic info"""
    name: str
    tricode: str
    logoUrl: str | None

class TeamScheduledGameInfoOut(BaseModel):
    """Output model for a team's upcoming game info"""
    id: int
    date: str
    homeTeam: TeamBasicInfoOut
    awayTeam: TeamBasicInfoOut
    predictedScore: dict = {"home": 0, "away": 0} # temporary until model
    time: datetime.datetime
    venue: str
    isNextGame: bool

class TeamRosteredPlayer(BaseModel):
    """Output model for a player on a team's roster"""
    id: int
    headshot: str
    first_name: str
    current_team_tri_code: str
    position: str
    last_name: str
    number: int | None
    shoots_catches: str

class TeamSearchResultOut(BaseModel):
    """Output model for a team search result"""
    name: str
    tricode: str
    logoUrl: str | None