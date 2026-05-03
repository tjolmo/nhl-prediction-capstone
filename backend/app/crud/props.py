from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models import Props
from app.schemas.player import PlayerPropOut

async def upsert_player_props(db: AsyncSession, props: list[PlayerPropOut]):
    data = [prop.model_dump() for prop in props]
    stmt = insert(Props).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['game_id', 'player_id', 'prop_type', 'over_under'],
        set_={
            "odds": stmt.excluded.odds,
            "line": stmt.excluded.line,
        }
    )
    await db.execute(stmt)
    await db.commit()