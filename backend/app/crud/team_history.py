from sqlalchemy.dialects.postgresql import insert
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