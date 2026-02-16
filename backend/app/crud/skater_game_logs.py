from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import SkaterGameLog
from external.moneypuck.response_models import SkaterGameLogResponse

async def upsert_scraped_game_log(db: AsyncSession, game_log_data: SkaterGameLogResponse):
    """Upserts scraped player game log into local db PlayerGameLogs table."""
    data = game_log_data.model_dump()
    stmt = insert(SkaterGameLog).values(**data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['game_id', 'player_id'],
        set_={
            "name": stmt.excluded.name,
            "season": stmt.excluded.season,
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