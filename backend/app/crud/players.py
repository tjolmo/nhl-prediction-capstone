from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Player
from external.response_models import PlayerResponse

async def upsert_scraped_player(db: AsyncSession, player_data: PlayerResponse, team_id: int | None = None):
    """Upserts scraped player into local db Players table."""
    data = player_data.model_dump()
    data["current_team_id"] = team_id
    stmt = insert(Player).values(**data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            "current_team_id": func.coalesce(stmt.excluded.current_team_id, Player.current_team_id),
            "headshot": stmt.excluded.headshot,
            "first_name": stmt.excluded.first_name,
            "last_name": stmt.excluded.last_name,
            "number": stmt.excluded.number,
            "position": stmt.excluded.position,
            "shoots_catches": stmt.excluded.shoots_catches,
        }
    )
    await db.execute(stmt)
    await db.commit()

async def get_player_by_id(db: AsyncSession, player_id: int) -> Player | None:
    """Fetches player from db by ID."""
    result = await db.execute(select(Player).where(Player.id == player_id))
    player = result.scalar_one_or_none()
    return player