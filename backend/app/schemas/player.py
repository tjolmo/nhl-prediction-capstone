from pydantic import BaseModel

class PlayerGameLogAddOut(BaseModel):
    player_id: int
    game_logs_added: int

    class Config:
        from_attributes = True

class PlayerGameLogGetOut(BaseModel):
    game_id: int
    player_id: int
    season: int
    name: str
    player_team_tricode: str
    opposing_team_tricode: str
    game_date: int
    goals: int
    primary_assists: int
    secondary_assists: int
    points: int
    x_goals: float
    toi: float
    high_danger_shots: int
    shot_attempts: int
    on_ice_x_goals_percentage: float
    game_score: float