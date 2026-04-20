import pandas as pd
from sqlalchemy import select, case
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SkaterGameFeatures, SkaterGameLog, Games, Player, GoalieGameFeatures, GoalieGameLog

async def load_skater_training_data(db: AsyncSession) -> pd.DataFrame:
    is_home_expr = case(
        (SkaterGameLog.home_away == "H", 1),
        else_=0,
    ).label("is_home")

    stmt = (
        select(
            SkaterGameFeatures.game_id,
            SkaterGameFeatures.player_id,
            SkaterGameFeatures.rolling_x_goals,
            SkaterGameFeatures.rolling_toi,
            SkaterGameFeatures.rolling_game_score,
            SkaterGameFeatures.rolling_shot_attempts,
            SkaterGameFeatures.rolling_high_danger_shots,
            SkaterGameFeatures.rolling_on_ice_x_goals_percentage,
            SkaterGameFeatures.rolling_primary_assists,
            SkaterGameFeatures.rolling_goals,
            SkaterGameFeatures.rolling_points,
            is_home_expr,
            SkaterGameLog.points,
            SkaterGameLog.goals,
            SkaterGameLog.primary_assists,
            SkaterGameLog.secondary_assists,
        )
        .join(
            SkaterGameLog,
            (SkaterGameFeatures.game_id == SkaterGameLog.game_id)
            & (SkaterGameFeatures.player_id == SkaterGameLog.player_id),
        )
    )
    result = await db.execute(stmt)
    rows = result.mappings().all()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)

async def load_skater_upcoming_features(db: AsyncSession) -> pd.DataFrame:
    is_home_expr = case(
        (Player.current_team_tri_code == Games.home_team_tri_code, 1),
        else_=0,
    ).label("is_home")
    stmt = (
        select(
            SkaterGameFeatures.game_id,
            SkaterGameFeatures.player_id,
            SkaterGameFeatures.rolling_x_goals,
            SkaterGameFeatures.rolling_toi,
            SkaterGameFeatures.rolling_game_score,
            SkaterGameFeatures.rolling_shot_attempts,
            SkaterGameFeatures.rolling_high_danger_shots,
            SkaterGameFeatures.rolling_on_ice_x_goals_percentage,
            SkaterGameFeatures.rolling_primary_assists,
            SkaterGameFeatures.rolling_goals,
            SkaterGameFeatures.rolling_points,
            is_home_expr,
        )
        .join(
            Games,
            SkaterGameFeatures.game_id == Games.id,
        )
        .join(
            Player,
            SkaterGameFeatures.player_id == Player.id,
        )
        .where(Games.game_state == "FUT")
    )
    result = await db.execute(stmt)
    rows = result.mappings().all()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)

async def load_goalie_training_data(db: AsyncSession) -> pd.DataFrame:
    is_home_expr = case(
        (GoalieGameLog.home_away == "H", 1),
        else_=0,
    ).label("is_home")

    stmt = (
        select(
            GoalieGameFeatures.game_id,
            GoalieGameFeatures.player_id,
            GoalieGameFeatures.rolling_x_goals_against,
            GoalieGameFeatures.rolling_goals_against,
            GoalieGameFeatures.rolling_sog,
            GoalieGameFeatures.rolling_flurry_adjusted_x_goals,
            GoalieGameFeatures.rolling_high_danger_x_goals,
            GoalieGameFeatures.rolling_x_sog,
            GoalieGameFeatures.rolling_high_danger_shots,
            GoalieGameFeatures.rolling_rebounds,
            GoalieGameFeatures.rolling_x_rebounds,
            GoalieGameFeatures.rolling_freeze,
            GoalieGameFeatures.rolling_x_freeze,
            is_home_expr,
            GoalieGameLog.goals_against,
            GoalieGameLog.sog,
        )
        .join(
            GoalieGameLog,
            (GoalieGameFeatures.game_id == GoalieGameLog.game_id)
            & (GoalieGameFeatures.player_id == GoalieGameLog.player_id),
        )
    )
    result = await db.execute(stmt)
    rows = result.mappings().all()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)

async def load_goalie_upcoming_features(db: AsyncSession) -> pd.DataFrame:
    is_home_expr = case(
        (Player.current_team_tri_code == Games.home_team_tri_code, 1),
        else_=0,
    ).label("is_home")

    stmt = (
        select(
            GoalieGameFeatures.game_id,
            GoalieGameFeatures.player_id,
            GoalieGameFeatures.rolling_x_goals_against,
            GoalieGameFeatures.rolling_goals_against,
            GoalieGameFeatures.rolling_sog,
            GoalieGameFeatures.rolling_flurry_adjusted_x_goals,
            GoalieGameFeatures.rolling_high_danger_x_goals,
            GoalieGameFeatures.rolling_x_sog,
            GoalieGameFeatures.rolling_high_danger_shots,
            GoalieGameFeatures.rolling_rebounds,
            GoalieGameFeatures.rolling_x_rebounds,
            GoalieGameFeatures.rolling_freeze,
            GoalieGameFeatures.rolling_x_freeze,
            is_home_expr,
        )
        .join(
            Games,
            GoalieGameFeatures.game_id == Games.id,
        )
        .join(
            Player,
            GoalieGameFeatures.player_id == Player.id,
        )
        .where(Games.game_state == "FUT")
    )
    result = await db.execute(stmt)
    rows = result.mappings().all()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)
