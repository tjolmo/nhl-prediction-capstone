from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import and_, exists, not_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TeamGameLog, SkaterGameLog, GoalieGameLog
from predictions.config import TEAM_BASE_STATS
import pandas as pd

async def upsert_team_game_logs(db: AsyncSession, game_logs: list[dict]):
    """Upserts aggregated team game logs into TeamGameLog table in batches."""
    if not game_logs:
        return
    for i in range(0, len(game_logs), 1000):
        batch = game_logs[i : i + 1000]
        stmt = insert(TeamGameLog).values(batch)
        stmt = stmt.on_conflict_do_update(
            index_elements=["game_id", "team_tri_code"],
            set_={
                "opposing_team_tri_code": stmt.excluded.opposing_team_tri_code,
                "season": stmt.excluded.season,
                "game_date": stmt.excluded.game_date,
                "home_away": stmt.excluded.home_away,
                "goals": stmt.excluded.goals,
                "x_goals": stmt.excluded.x_goals,
                "shot_attempts": stmt.excluded.shot_attempts,
                "high_danger_shots": stmt.excluded.high_danger_shots,
                "points": stmt.excluded.points,
                "primary_assists": stmt.excluded.primary_assists,
                "avg_on_ice_x_goals_percentage": stmt.excluded.avg_on_ice_x_goals_percentage,
                "avg_game_score": stmt.excluded.avg_game_score,
                "goals_against": stmt.excluded.goals_against,
                "x_goals_against": stmt.excluded.x_goals_against,
                "sog_against": stmt.excluded.sog_against,
                "high_danger_shots_against": stmt.excluded.high_danger_shots_against,
                "high_danger_x_goals_against": stmt.excluded.high_danger_x_goals_against,
                "flurry_adjusted_x_goals_against": stmt.excluded.flurry_adjusted_x_goals_against,
            }
        )
        await db.execute(stmt)
    await db.commit()

async def calculate_rolling_features_for_team(db: AsyncSession, tri_code: str, season: int) -> pd.DataFrame:
    """Calculates rolling features for a team based on their last 5 games."""

    query = select(
        *[getattr(TeamGameLog, s) for s in TEAM_BASE_STATS],
    ).where(
        TeamGameLog.team_tri_code == tri_code,
        TeamGameLog.season == season
    ).order_by(
        TeamGameLog.game_date.desc()
    ).limit(5)
    
    result = await db.execute(query)
    rows = result.mappings().all()

    if len(rows) < 5:
        return pd.DataFrame()

    games = pd.DataFrame(rows)

    features: dict[str, float] = {
        f"rolling_{stat}_5g": float(games[stat].mean())
        for stat in TEAM_BASE_STATS
    }

    return pd.DataFrame(features, index=[0])

async def build_team_game_logs(db: AsyncSession) -> None:
    """Aggregate skater + goalie game logs into team-level game logs."""

    offense_sub = (
        select(
            SkaterGameLog.game_id,
            SkaterGameLog.player_team_tricode.label("team_tri_code"),
            SkaterGameLog.opposing_team_tricode.label("opposing_team_tri_code"),
            SkaterGameLog.season,
            SkaterGameLog.game_date,
            SkaterGameLog.home_away,
            func.sum(SkaterGameLog.goals).label("goals"),
            func.sum(SkaterGameLog.x_goals).label("x_goals"),
            func.sum(SkaterGameLog.shot_attempts).label("shot_attempts"),
            func.sum(SkaterGameLog.high_danger_shots).label("high_danger_shots"),
            func.sum(SkaterGameLog.points).label("points"),
            func.sum(SkaterGameLog.primary_assists).label("primary_assists"),
            func.avg(SkaterGameLog.on_ice_x_goals_percentage).label("avg_on_ice_x_goals_percentage"),
            func.avg(SkaterGameLog.game_score).label("avg_game_score"),
        )
        .group_by(
            SkaterGameLog.game_id,
            SkaterGameLog.player_team_tricode,
            SkaterGameLog.opposing_team_tricode,
            SkaterGameLog.season,
            SkaterGameLog.game_date,
            SkaterGameLog.home_away,
        )
        .subquery("offense")
    )

    # finds starting goalie (max TOI)
    goalie_toi_sub = (
        select(
            GoalieGameLog.game_id,
            GoalieGameLog.player_team_tricode.label("team_tri_code"),
            func.max(GoalieGameLog.toi).label("max_toi"),
        )
        .group_by(GoalieGameLog.game_id, GoalieGameLog.player_team_tricode)
        .subquery("goalie_toi")
    )

    defense_sub = (
        select(
            GoalieGameLog.game_id,
            GoalieGameLog.player_team_tricode.label("team_tri_code"),
            GoalieGameLog.goals_against,
            GoalieGameLog.x_goals_against,
            GoalieGameLog.sog.label("sog_against"),
            GoalieGameLog.high_danger_shots.label("high_danger_shots_against"),
            GoalieGameLog.high_danger_x_goals.label("high_danger_x_goals_against"),
            GoalieGameLog.flurry_adjusted_x_goals.label("flurry_adjusted_x_goals_against"),
        )
        .join(
            goalie_toi_sub,
            and_(
                GoalieGameLog.game_id == goalie_toi_sub.c.game_id,
                GoalieGameLog.player_team_tricode == goalie_toi_sub.c.team_tri_code,
                GoalieGameLog.toi == goalie_toi_sub.c.max_toi,
            ),
        )
        .subquery("defense")
    )

    combined_query = (
        select(
            offense_sub.c.game_id,
            offense_sub.c.team_tri_code,
            offense_sub.c.opposing_team_tri_code,
            offense_sub.c.season,
            offense_sub.c.game_date,
            offense_sub.c.home_away,
            offense_sub.c.goals,
            offense_sub.c.x_goals,
            offense_sub.c.shot_attempts,
            offense_sub.c.high_danger_shots,
            offense_sub.c.points,
            offense_sub.c.primary_assists,
            offense_sub.c.avg_on_ice_x_goals_percentage,
            offense_sub.c.avg_game_score,
            defense_sub.c.goals_against,
            defense_sub.c.x_goals_against,
            defense_sub.c.sog_against,
            defense_sub.c.high_danger_shots_against,
            defense_sub.c.high_danger_x_goals_against,
            defense_sub.c.flurry_adjusted_x_goals_against,
        )
        .join(
            defense_sub,
            and_(
                offense_sub.c.game_id == defense_sub.c.game_id,
                offense_sub.c.team_tri_code == defense_sub.c.team_tri_code,
            ),
        )
        .where(
            not_(
                exists().where(
                    (TeamGameLog.game_id == offense_sub.c.game_id) &
                    (TeamGameLog.team_tri_code == offense_sub.c.team_tri_code)
                )
            )
        )
    )

    result = await db.execute(combined_query)
    new_team_logs = [dict(row) for row in result.mappings().all()]

    if new_team_logs:
        await upsert_team_game_logs(db, new_team_logs)
    