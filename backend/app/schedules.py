from sqlalchemy.ext.asyncio import AsyncSession
from external.nhl.teams import fetch_and_clean_team, fetch_and_clean_team_roster
from .crud.team_history import upsert_team_history, check_team_history_exists_and_updated
from .crud.teams import upsert_team, get_all_tri_codes_update_roster
from .crud.players import upsert_scraped_player
CURRENT_TEAMS = [
        8, 7, 2, 28, 13, 12, 54, 52, 
        18, 1, 9, 21, 15, 26, 10, 22,
        20, 19, 17, 3, 24, 23, 16, 55, 
        5, 6, 25, 14, 4, 30, 68, 29, 53 #ari
]
OLD_TEAMS = [59] #uhc

async def add_current_teams_to_db(db: AsyncSession):
    for team_id in CURRENT_TEAMS:
        if not await check_team_history_exists_and_updated(db, team_id):
            team_data, team_history_data = await fetch_and_clean_team(team_id)
            if team_data and team_history_data:
                await upsert_team(db, team_data)
                await upsert_team_history(db, team_history_data)
        else:
            print(f"Team history for team ID {team_id} already exists in DB, skipping.")

async def add_old_teams_to_db(db: AsyncSession):
    for team_id in OLD_TEAMS:
        if not await check_team_history_exists_and_updated(db, team_id):
            _, team_history_data = await fetch_and_clean_team(team_id)
            if team_history_data:
                await upsert_team_history(db, team_history_data)
        else:
            print(f"Team history for team ID {team_id} already exists in DB, skipping.")

async def fetch_current_rosters_for_all_teams(db: AsyncSession):
    tri_codes = await get_all_tri_codes_update_roster(db)
    for tri_code in tri_codes:
        roster_data = await fetch_and_clean_team_roster(tri_code, "current")
        if roster_data:
            for player in roster_data:
                await upsert_scraped_player(db, player, tri_code)
        