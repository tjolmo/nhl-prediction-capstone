from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TeamHistory
from external.response_models import TeamHistoryResponse
import datetime

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

async def check_team_history_exists_and_updated(db: AsyncSession, team_id: int) -> bool:
    """Checks if team history with the given team ID exists in the database."""
    result = await db.execute(select(TeamHistory).where(TeamHistory.id == team_id))
    team_history = result.scalar_one_or_none()
    if team_history:
        # If the team history exists, check if it was updated in the last day
        if team_history.last_updated and (datetime.datetime.now() - team_history.last_updated).days < 1:
            return True
    return False