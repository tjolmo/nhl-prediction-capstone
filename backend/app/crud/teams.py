from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Team
from external.response_models import TeamResponse

async def upsert_team(db: AsyncSession, team_data: TeamResponse):
    """Upserts scraped team into local db Teams table."""
    data = team_data.model_dump()
    stmt = insert(Team).values(**data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['tri_code'],
        set_={
            "franchise_id": stmt.excluded.franchise_id,
            "current_name": stmt.excluded.current_name,
        }
    )
    await db.execute(stmt)
    await db.commit()

async def get_team_by_id(db: AsyncSession, team_id: int) -> Team | None:
    """Fetches team from db by ID."""
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalar_one_or_none()
    return team

async def get_team_tricode_from_id(db: AsyncSession, team_id: int) -> str | None:
    """Fetches team tri code from db by ID."""
    result = await db.execute(select(Team.tri_code).where(Team.id == team_id))
    tri_code = result.scalar_one_or_none()
    return tri_code