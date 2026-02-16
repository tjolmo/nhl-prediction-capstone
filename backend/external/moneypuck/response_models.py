from pydantic import BaseModel, Field

class SkaterGameLogResponse(BaseModel):
    game_id: int = Field(alias="gameId")
    player_id: int = Field(alias="playerId")
    season: int = Field(alias="season")
    name: str = Field (alias="name")
    player_team_tricode: str = Field(alias="playerTeam")
    opposing_team_tricode: str = Field(alias="opposingTeam")
    game_date: int = Field(alias="gameDate")
    goals: int = Field(alias="I_F_goals")
    primary_assists: int = Field(alias="I_F_primaryAssists")
    secondary_assists: int = Field(alias="I_F_secondaryAssists")
    points: int = Field(alias="I_F_points")
    x_goals: float = Field(alias="I_F_xGoals")
    toi: float = Field(alias="icetime")
    high_danger_shots: int = Field(alias="I_F_highDangerShots")
    shot_attempts: int = Field(alias="I_F_shotAttempts")
    on_ice_x_goals_percentage: float = Field(alias="onIce_xGoalsPercentage")
    game_score: float = Field(alias="gameScore")

    class Config:
        validate_by_name = True