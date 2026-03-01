from sqlalchemy.ext.asyncio import AsyncSession

from external.nhl.players import fetch_and_get_players_info
from .crud.goalie_game_logs import get_goalie_most_recent_game_date_and_last_updated
from external.nhl.teams import fetch_and_clean_team, fetch_and_clean_team_roster, fetch_and_clean_team_schedule
from external.nhl.games import fetch_and_get_players_in_a_game
from external.moneypuck.player import scrape_skater_game_data, scrape_goalie_game_data
from .crud.team_history import upsert_team_history, check_team_history_exists_and_updated
from .crud.teams import get_all_tri_codes_in_db, upsert_team, get_all_tri_codes_update_roster, update_team_roster_last_updated
from .crud.games import check_if_games_in_db, get_date_most_recent_game_played, upsert_scraped_game_from_schedule, get_date_most_recent_game_marked_as_future
from .crud.players import get_all_goalie_ids_and_teams, get_all_skater_ids_and_teams, get_players_not_in_db, upsert_scraped_player, set_all_other_players_current_team_tri_code_to_null
from .crud.skater_game_logs import get_player_most_recent_game_date_and_last_updated, upsert_scraped_game_log
from .crud.goalie_game_logs import upsert_scraped_goalie_game_log
import datetime

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
    players_updated = []
    for tri_code in tri_codes:
        roster_data = await fetch_and_clean_team_roster(tri_code, "current")
        if roster_data:
            for player in roster_data:
                await upsert_scraped_player(db, player, tri_code)
                players_updated.append(player.id)
            await update_team_roster_last_updated(db, tri_code)
    await set_all_other_players_current_team_tri_code_to_null(db, players_updated)
        
async def fetch_current_schedules_for_all_teams(db: AsyncSession):
    tri_codes = await get_all_tri_codes_in_db(db)
    for tri_code in tri_codes:
        current_marked_upcoming_date = await get_date_most_recent_game_marked_as_future(db, tri_code)
        # only fetch and update if current time(UTC) more recent
        current_time = datetime.datetime.now(datetime.timezone.utc)
        if current_marked_upcoming_date is None or current_time >= current_marked_upcoming_date:
            schedule_data = await fetch_and_clean_team_schedule(tri_code, "now")
            if schedule_data:
                for game in schedule_data:
                    await upsert_scraped_game_from_schedule(db, game)

async def fetch_past_two_seasons_schedules_for_all_teams(db: AsyncSession):
    tri_codes = await get_all_tri_codes_in_db(db)
    for season in ["20232024", "20242025", "now"]:
        all_schedule_data = set()
        for tri_code in tri_codes:
            schedule_data = await fetch_and_clean_team_schedule(tri_code, season)
            if schedule_data:
                all_schedule_data.update(schedule_data)
        # once all schedules fetched, process
        all_players_in_season = set()
        # limit to games not in db already
        games_in_db = await check_if_games_in_db(db, [game.id for game in all_schedule_data])
        schedule_data_to_add = [game for game in all_schedule_data if game.id not in games_in_db]

        for game in schedule_data_to_add:
            # fetch players in game, 
            players_in_game = await fetch_and_get_players_in_a_game(game.id)
            if players_in_game:
                all_players_in_season.update(players_in_game)

        # check which players not in db, fetch info for those players and add to db
        if all_players_in_season:
            players_not_in_db = await get_players_not_in_db(db, list(all_players_in_season))
            for player_id in players_not_in_db:
                player_info = await fetch_and_get_players_info(player_id)
                if player_info:
                    await upsert_scraped_player(db, player_info, None)
    
        # add every game to db after player scrape to ensure that players added first
        for game in schedule_data_to_add:
            await upsert_scraped_game_from_schedule(db, game)

async def fetch_skater_all_game_logs_for_recent_games(db: AsyncSession):
    """Fetches and upserts skater game logs for recent games for a team by tri code."""
    game_logs = None
    players = await get_all_skater_ids_and_teams(db)
    for player in players:
        player_id = player[0]
        tri_code = player[1]

        # date as int YYYYMMDD
        latest_game: int = await get_date_most_recent_game_played(db, tri_code)
        if latest_game:
            #convert to utc dtime YYYYMMDD int to datetime with utc timezone
            latest_game_datetime = datetime.datetime.strptime(str(latest_game), "%Y%m%d").replace(tzinfo=datetime.timezone.utc)

        skater_info = await get_player_most_recent_game_date_and_last_updated(db, player_id)
        if skater_info:
            latest_game_log_date = skater_info[0]
            last_updated = skater_info[1]

            if latest_game and \
                (latest_game > latest_game_log_date) and \
                (latest_game_datetime > last_updated):
                # scrape just recent logs
                game_logs = scrape_skater_game_data(player_id, latest_game)
        else:
            #scrape all if player has no game logs in db
            game_logs = scrape_skater_game_data(player_id)

        #upsert to db
        if game_logs:
            for game_log in game_logs:
                await upsert_scraped_game_log(db, game_log)

async def fetch_goalie_all_game_logs_for_recent_games(db: AsyncSession):
    """Fetches and upserts goalie game logs for recent games for a team by tri code."""
    
    #get all tri codes
    tri_codes = await get_all_tri_codes_in_db(db)
    for tri_code in tri_codes:
        # date as int YYYYMMDD
        latest_game: int = await get_date_most_recent_game_played(db, tri_code)
        if latest_game:
            #convert to utc dtime YYYYMMDD int to datetime with utc timezone
            latest_game_datetime = datetime.datetime.strptime(str(latest_game), "%Y%m%d").replace(tzinfo=datetime.timezone.utc)


    game_logs = None
    players = await get_all_goalie_ids_and_teams(db)
    for player in players:
        player_id = player[0]
        tri_code = player[1]

        # date as int YYYYMMDD
        latest_game: int = await get_date_most_recent_game_played(db, tri_code)
        if latest_game:
            #convert to utc dtime YYYYMMDD int to datetime with utc timezone
            latest_game_datetime = datetime.datetime.strptime(str(latest_game), "%Y%m%d").replace(tzinfo=datetime.timezone.utc)

        goalie_info = await get_goalie_most_recent_game_date_and_last_updated(db, player_id)
        if goalie_info:
            latest_game_log_date = goalie_info[0]
            last_updated = goalie_info[1]

            if latest_game and \
                (latest_game > latest_game_log_date) and \
                (latest_game_datetime > last_updated):
                # scrape just recent logs
                game_logs = scrape_goalie_game_data(player_id, latest_game)
        else:
            #scrape all if player has no game logs in db
            game_logs = scrape_goalie_game_data(player_id)

        #upsert to db
        if game_logs:
            for game_log in game_logs:
                await upsert_scraped_goalie_game_log(db, game_log)