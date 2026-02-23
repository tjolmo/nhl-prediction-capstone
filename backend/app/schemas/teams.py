from pydantic import BaseModel

class TeamInfoOut(BaseModel):
    id: int
    name: str
    franchise_id: int
    tri_code: str

    class Config:
        from_attributes = True

class TeamRosterAddOut(BaseModel):
    team: str
    season: str
    roster_added: bool
    num_players_added: int

    class Config:
        from_attributes = True

class TeamScheduleAddOut(BaseModel):
    team: str
    season: str
    num_games_added: int

    class Config:
        from_attributes = True

class Last5GameInfoOut(BaseModel):
    game_id: int
    date: int
    home_team_tri_code: str
    away_team_tri_code: str
    home_score: int | None
    away_score: int | None

    class Config:
        from_attributes = True