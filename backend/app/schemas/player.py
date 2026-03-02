import datetime

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
    home_away: str
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

    class Config:
        from_attributes = True

class GoalieGameLogGetOut(BaseModel):
    game_id: int
    player_id: int
    season: int
    name: str
    home_away: str
    player_team_tricode: str
    opposing_team_tricode: str
    game_date: int
    toi: float
    x_goals_against: float
    goals_against: int
    unblocked_shot_attempts: int
    x_rebounds: float
    rebounds: int
    x_freeze: float
    freeze: int
    x_sog: float
    sog: int
    x_play_stopped: float
    play_stopped: int
    x_play_continued_in_zone: float
    x_play_continued_outside_zone: float
    flurry_adjusted_x_goals: float
    low_danger_shots: int
    medium_danger_shots: int
    high_danger_shots: int
    low_danger_x_goals: float
    medium_danger_x_goals: float
    high_danger_x_goals: float
    blocked_shot_attempts: int
    penality_minutes: int
    penalties: int

    class Config:
        from_attributes = True

class SkaterSeasonBasicStatsGetOut(BaseModel):
    games: int
    goals: int
    assists: int
    points: int

class SkaterLast5BasicStatsGetOut(BaseModel):
    date: str | None
    opposing_team_tricode: str
    goals: int
    assists: int
    points: int
    home_away: str

class PlayerBasicInfoOut(BaseModel):
    name: str
    number: int | None
    position: str
    team: str
    headshotUrl: str

class PlayerNextGameGetOut(BaseModel):
    date: str | None
    opposing_team_tricode: str
    venue: str
    time: datetime.datetime
    home_away: str

class GoalieLast5BasicStatsGetOut(BaseModel):
    date: str | None
    opposing_team_tricode: str
    saves: int
    goals_against: int
    save_percentage: float
    home_away: str

class GoalieSeasonBasicStatsGetOut(BaseModel):
    games: int
    gaa: float
    save_percentage: float