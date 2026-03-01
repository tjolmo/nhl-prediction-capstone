from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import GoalieGameLog
from external.moneypuck.response_models import GoalieGameLogResponse
import datetime

async def upsert_scraped_goalie_game_logs(db: AsyncSession, game_logs_data: list[GoalieGameLogResponse]):
    """Upserts scraped goale game logs into local db GoalieGameLogs table."""
    if not game_logs_data:
        return
    data = [log.model_dump() for log in game_logs_data]
    stmt = insert(GoalieGameLog).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['game_id', 'player_id'],
        set_={
            "name": stmt.excluded.name,
            "season": stmt.excluded.season,
            "home_away": stmt.excluded.home_away,
            "player_team_tricode": stmt.excluded.player_team_tricode,
            "opposing_team_tricode": stmt.excluded.opposing_team_tricode,
            "game_date": stmt.excluded.game_date,
            "toi": stmt.excluded.toi,
            "x_goals_against": stmt.excluded.x_goals_against,
            "goals_against": stmt.excluded.goals_against,
            "unblocked_shot_attempts": stmt.excluded.unblocked_shot_attempts,
            "x_rebounds": stmt.excluded.x_rebounds,
            "rebounds": stmt.excluded.rebounds,
            "x_freeze": stmt.excluded.x_freeze,
            "freeze": stmt.excluded.freeze,
            "x_sog": stmt.excluded.x_sog,
            "sog": stmt.excluded.sog,
            "x_play_stopped": stmt.excluded.x_play_stopped,
            "play_stopped": stmt.excluded.play_stopped,
            "x_play_continued_in_zone": stmt.excluded.x_play_continued_in_zone,
            "x_play_continued_outside_zone": stmt.excluded.x_play_continued_outside_zone,
            "flurry_adjusted_x_goals": stmt.excluded.flurry_adjusted_x_goals,
            "low_danger_shots": stmt.excluded.low_danger_shots,
            "medium_danger_shots": stmt.excluded.medium_danger_shots,
            "high_danger_shots": stmt.excluded.high_danger_shots,
            "low_danger_x_goals": stmt.excluded.low_danger_x_goals,
            "medium_danger_x_goals": stmt.excluded.medium_danger_x_goals,
            "high_danger_x_goals": stmt.excluded.high_danger_x_goals,
            "blocked_shot_attempts": stmt.excluded.blocked_shot_attempts,
            "penality_minutes": stmt.excluded.penality_minutes,
            "penalties": stmt.excluded.penalties,
        }
    )
    await db.execute(stmt)
    await db.commit()

async def get_goalie_game_log_by_game_and_player_id(db: AsyncSession, game_id: int, player_id: int) -> GoalieGameLog | None:
    """Fetches goalie game log from db by game ID and player ID."""
    result = await db.execute(
        select(GoalieGameLog).where(
            GoalieGameLog.game_id == game_id,
            GoalieGameLog.player_id == player_id
        )
    )
    game_log = result.scalar_one_or_none()
    return game_log


async def get_goalie_most_recent_game_date_and_last_updated(db: AsyncSession, player_id: int) -> tuple[int, datetime.datetime] | None:
    """Fetches most recent game date from db for a goalie by player ID."""
    result = await db.execute(
        select(GoalieGameLog.game_date, GoalieGameLog.last_updated).
        where(GoalieGameLog.player_id == player_id).
        order_by(GoalieGameLog.game_date.desc()).
        limit(1)
    )
    game_date_and_last_updated = result.one_or_none()
    return game_date_and_last_updated

async def get_all_goalies_need_update(db: AsyncSession, team_tri_code: str, latest_game_date: int) -> list[tuple[int, str]]:
    """Fetches all goalie IDs w team from the database that need game log updates."""
    # filter to most recent game log for goalie
    result = await db.execute(
        select(GoalieGameLog.player_id, GoalieGameLog.player_team_tricode).
        where(
            GoalieGameLog.player_team_tricode == team_tri_code,
            GoalieGameLog.game_date == latest_game_date
        ).
        order_by(GoalieGameLog.game_date.desc())
    )