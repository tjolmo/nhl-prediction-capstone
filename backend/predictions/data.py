import pandas as pd
from sqlalchemy import select, case
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SkaterGameFeatures, SkaterGameLog, GoalieGameFeatures, GoalieGameLog, TeamGameFeatures, TeamGameLog

async def load_skater_training_data(db: AsyncSession) -> pd.DataFrame:
    is_home_expr = case(
        (SkaterGameLog.home_away == "HOME", 1),
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

async def load_goalie_training_data(db: AsyncSession) -> pd.DataFrame:
    is_home_expr = case(
        (GoalieGameLog.home_away == "HOME", 1),
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

async def load_team_training_data(db: AsyncSession) -> pd.DataFrame:
    is_home_expr = case(
        (TeamGameLog.home_away == "HOME", 1),
        else_=0,
    ).label("is_home")

    _BASE_STATS = [
        "goals", "x_goals", "shot_attempts", "high_danger_shots",
        "points", "primary_assists", "avg_on_ice_x_goals_percentage",
        "avg_game_score", "goals_against", "x_goals_against",
        "sog_against", "high_danger_shots_against",
        "high_danger_x_goals_against", "flurry_adjusted_x_goals_against",
    ]

    self_feature_cols = []
    opp_feature_cols = []
    OppFeatures = aliased(TeamGameFeatures)

    for stat in _BASE_STATS:
        col_name = f"rolling_{stat}_5g"
        self_feature_cols.append(getattr(TeamGameFeatures, col_name))
        opp_feature_cols.append(
            getattr(OppFeatures, col_name).label(f"opp_{col_name}")
        )

    stmt = (
        select(
            TeamGameFeatures.game_id,
            TeamGameFeatures.team_tri_code,
            *self_feature_cols,
            is_home_expr,
            *opp_feature_cols,
            TeamGameLog.goals,
            TeamGameLog.goals_against,
        )
        .join(
            TeamGameLog,
            (TeamGameFeatures.game_id == TeamGameLog.game_id)
            & (TeamGameFeatures.team_tri_code == TeamGameLog.team_tri_code),
        )
        .join(
            OppFeatures,
            (TeamGameFeatures.game_id == OppFeatures.game_id)
            & (TeamGameFeatures.team_tri_code != OppFeatures.team_tri_code),
        )
    )
    result = await db.execute(stmt)
    rows = result.mappings().all()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)
