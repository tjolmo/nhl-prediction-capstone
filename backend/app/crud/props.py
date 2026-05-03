from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func
from app.models import Props
from app.schemas.player import PlayerPropOut

async def upsert_player_props(db: AsyncSession, props: list[PlayerPropOut]):
    """Upserts player props from Odds api to db"""
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

async def get_player_props_from_db(db: AsyncSession, player_id: int) -> list[PlayerPropOut]:
    """Gets most recent player props for a player from the database."""
    latest_game_id = (
        select(func.max(Props.game_id))
        .where(Props.player_id == player_id)
        .scalar_subquery()
    )

    stmt = (
        select(Props)
        .where(
            Props.player_id == player_id,
            Props.game_id == latest_game_id
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()