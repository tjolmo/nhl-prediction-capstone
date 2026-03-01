from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Player
from external.nhl.response_models import PlayerResponse, PlayerLandingResponse
import datetime

async def upsert_scraped_player(db: AsyncSession, player_data: PlayerResponse|PlayerLandingResponse, tri_code: str | None = None):
    """Upserts scraped player into local db Players table."""
    data = player_data.model_dump()
    data["current_team_tri_code"] = tri_code
    stmt = insert(Player).values(**data)
    stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            "current_team_tri_code": func.coalesce(stmt.excluded.current_team_tri_code, Player.current_team_tri_code),
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

async def get_skater_by_id(db: AsyncSession, player_id: int) -> Player | None:
    """Fetches player from db by ID."""
    result = await db.execute(select(Player).where(Player.id == player_id, Player.position != "G"))
    player = result.scalar_one_or_none()
    return player

async def get_goalie_by_id(db: AsyncSession, player_id: int) -> Player | None:
    """Fetches goalie from db by ID."""
    result = await db.execute(select(Player).where(Player.id == player_id, Player.position == "G"))
    player = result.scalar_one_or_none()
    return player

async def update_player_game_log_last_updated(db: AsyncSession, player_id: int):
    """Updates the game_log_last_updated field for a player."""
    stmt = (
        update(Player).
        where(Player.id == player_id).
        values(game_log_last_updated=datetime.datetime.now(datetime.timezone.utc))
    )
    await db.execute(stmt)
    await db.commit()

async def get_all_skater_ids_and_teams(db: AsyncSession) -> list[tuple[int, str]]:
    """Fetches all skater IDs w team from the database."""
    result = await db.execute(
        select(Player.id, Player.current_team_tri_code).where(
            Player.position != "G"
        )
    )
    player_ids = result.all()
    return player_ids

async def get_all_skaters_on_a_roster(db: AsyncSession) -> list[tuple[int, str]]:
    """Fetches all skaters on a roster for a team by tri code."""
    result = await db.execute(
        select(Player.id, Player.current_team_tri_code).where(
            Player.current_team_tri_code != None,
            Player.position != "G"
        )
    )
    players = result.scalars().all()
    return players

async def get_all_goalies_on_a_roster(db: AsyncSession) -> list[tuple[int, str]]:
    """Fetches all goalies on a roster for a team by tri code."""
    result = await db.execute(
        select(Player.id, Player.current_team_tri_code).where(
            Player.current_team_tri_code != None,
            Player.position == "G"
        )
    )
    players = result.scalars().all()
    return players

async def get_all_goalie_ids_and_teams(db: AsyncSession) -> list[tuple[int, str]]:
    """Fetches all goalie IDs w team from the database."""
    result = await db.execute(
        select(Player.id, Player.current_team_tri_code).where(
            Player.position == "G"
        )
    )
    player_ids = result.all()
    return player_ids

async def get_players_not_in_db(db: AsyncSession, player_ids: list[int]) -> list[int]:
    """Fetches player IDs not in the database."""
    result = await db.execute(
        select(Player.id).where(Player.id.in_(player_ids))
    )
    existing_player_ids = result.scalars().all()
    return [player_id for player_id in player_ids if player_id not in existing_player_ids]


async def set_all_other_players_current_team_tri_code_to_null(db: AsyncSession, player_ids_on_current_roster: list[int]):
    """Sets current_team_tri_code to null for all players not on the current roster for a team."""
    stmt = (
        update(Player).
        where(Player.id.not_in(player_ids_on_current_roster)).
        values(current_team_tri_code=None)
    )
    await db.execute(stmt)
    await db.commit()