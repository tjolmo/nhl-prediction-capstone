from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TeamHistory
from external.response_models import TeamHistoryResponse

async def upsert_team_history(db: AsyncSession, team_history_data: TeamHistoryResponse):
    """Upserts scraped team history data into local db TeamHistory table."""
    data = team_history_data.model_dump()
    stmt = insert(TeamHistory).values(**data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            "name": stmt.excluded.name,
            "tri_code": stmt.excluded.tri_code,
        }
    )
    await db.execute(stmt)
    await db.commit()

async def check_team_history_exists(db: AsyncSession, team_id: int) -> bool:
    """Checks if team history with the given team ID exists in the database."""
    result = await db.execute(select(TeamHistory).where(TeamHistory.id == team_id))
    team_history = result.scalar_one_or_none()
    return team_history is not None