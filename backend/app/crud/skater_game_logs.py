from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import SkaterGameLog
from external.moneypuck.response_models import SkaterGameLogResponse
import datetime

async def upsert_scraped_game_logs(db: AsyncSession, game_logs_data: list[SkaterGameLogResponse]):
    """Upserts scraped player game log into local db PlayerGameLogs table."""
    if not game_logs_data:
        return
    data = [log.model_dump() for log in game_logs_data]
    stmt = insert(SkaterGameLog).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['game_id', 'player_id'],
        set_={
            "name": stmt.excluded.name,
            "season": stmt.excluded.season,
            "home_away": stmt.excluded.home_away,
            "player_team_tricode": stmt.excluded.player_team_tricode,
            "opposing_team_tricode": stmt.excluded.opposing_team_tricode,
            "game_date": stmt.excluded.game_date,
            "goals": stmt.excluded.goals,
            "primary_assists": stmt.excluded.primary_assists,
            "secondary_assists": stmt.excluded.secondary_assists,
            "points": stmt.excluded.points,
            "x_goals": stmt.excluded.x_goals,
            "toi": stmt.excluded.toi,
            "high_danger_shots": stmt.excluded.high_danger_shots,
            "shot_attempts": stmt.excluded.shot_attempts,
            "on_ice_x_goals_percentage": stmt.excluded.on_ice_x_goals_percentage,
            "game_score": stmt.excluded.game_score,
        }
    )
    await db.execute(stmt)
    await db.commit()

async def get_player_game_log_by_game_and_player_id(db: AsyncSession, game_id: int, player_id: int) -> SkaterGameLog | None:
    """Fetches player game log from db by game ID and player ID."""
    result = await db.execute(
        select(SkaterGameLog).where(
            SkaterGameLog.game_id == game_id,
            SkaterGameLog.player_id == player_id
        )
    )
    game_log = result.scalar_one_or_none()
    return game_log

async def get_player_most_recent_game_date_and_last_updated(db: AsyncSession, player_id: int) -> tuple[int, datetime.datetime] | None:
    """Fetches most recent game date from db for a player by player ID."""
    result = await db.execute(
        select(SkaterGameLog.game_date, SkaterGameLog.last_updated).
        where(SkaterGameLog.player_id == player_id).
        order_by(SkaterGameLog.game_date.desc()).
        limit(1)
    )
    game_date_and_last_updated = result.one_or_none()
    return game_date_and_last_updated

