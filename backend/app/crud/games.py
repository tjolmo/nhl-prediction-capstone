from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Games
from external.nhl.response_models import GameResponse
import datetime
async def upsert_scraped_game_from_schedule(db: AsyncSession, game_data: GameResponse):
    """Upserts scraped game into local db Games table."""
    data = game_data.model_dump()
    stmt = insert(Games).values(**data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            "home_team_tri_code": stmt.excluded.home_team_tri_code,
            "away_team_tri_code": stmt.excluded.away_team_tri_code,
            "season": stmt.excluded.season,
            "date": stmt.excluded.date,
            "venue": stmt.excluded.venue,
            "start_time": stmt.excluded.start_time,
            "home_team_logo": stmt.excluded.home_team_logo,
            "away_team_logo": stmt.excluded.away_team_logo,
            "home_score": stmt.excluded.home_score,
            "away_score": stmt.excluded.away_score,
            "game_state": stmt.excluded.game_state,
            "last_updated": datetime.datetime.now(datetime.timezone.utc),
        }
    )
    await db.execute(stmt)
    await db.commit()

async def get_team_last_5_games(db: AsyncSession, tri_code: str) -> list[Games]:
    """Fetches last 5 games from db for a team by tri code and season."""
    result = await db.execute(
        select(Games).
        where(
            (Games.home_team_tri_code == tri_code) | (Games.away_team_tri_code == tri_code),
            (Games.game_state == "OFF")
        ).
        order_by(Games.date.desc()).
        limit(5)
    )
    games = result.scalars().all()
    return games