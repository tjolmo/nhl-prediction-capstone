from app.crud.goalie_game_features import update_goalie_game_features
from app.crud.skater_game_features import update_skater_game_features
from external.moneypuck.player import scrape_all_goalie_game_logs, scrape_all_skater_game_logs
from external.nhl.players import fetch_and_get_players_info
from external.nhl.teams import fetch_and_clean_team, fetch_and_clean_team_roster, fetch_and_clean_team_schedule
from external.nhl.games import fetch_and_get_players_in_a_game, get_current_scores
from .crud.team_history import upsert_team_history, check_team_history_exists_and_updated
from .crud.teams import get_all_tri_codes_in_db, upsert_team,update_team_roster_last_updated, get_all_tri_codes_update_roster
from .crud.games import check_if_games_in_db, upsert_scraped_games_from_schedule, get_date_most_recent_game_marked_as_future, delete_games_for_team_in_the_future
from .crud.players import get_players_not_in_db, upsert_scraped_player, set_all_other_players_current_team_tri_code_to_null
from .crud.skater_game_logs import upsert_scraped_game_logs
from .crud.goalie_game_logs import upsert_scraped_goalie_game_logs
from app.database import AsyncSessionLocal
import datetime

CURRENT_TEAMS = [
        8, 7, 2, 28, 13, 12, 54, 52, 
        18, 1, 9, 21, 15, 26, 10, 22,
        20, 19, 17, 3, 24, 23, 16, 55, 
        5, 6, 25, 14, 4, 30, 68, 29, 53 #ari
]
OLD_TEAMS = [59] #uhc

async def add_current_teams_to_db():
    async with AsyncSessionLocal() as db:
        for team_id in CURRENT_TEAMS:
            if not await check_team_history_exists_and_updated(db, team_id):
                team_data, team_history_data = await fetch_and_clean_team(team_id)
                if team_data and team_history_data:
                    await upsert_team(db, team_data)
                    await upsert_team_history(db, team_history_data)
            else:
                print(f"Team history for team ID {team_id} already exists in DB, skipping.")

async def add_old_teams_to_db():
    async with AsyncSessionLocal() as db:
        for team_id in OLD_TEAMS:
            if not await check_team_history_exists_and_updated(db, team_id):
                _, team_history_data = await fetch_and_clean_team(team_id)
                if team_history_data:
                    await upsert_team_history(db, team_history_data)
            else:
                print(f"Team history for team ID {team_id} already exists in DB, skipping.")

async def fetch_current_rosters_for_all_teams():
    async with AsyncSessionLocal() as db:
        tri_codes = await get_all_tri_codes_update_roster(db)
        tri_codes = await get_all_tri_codes_in_db(db)
        players_updated = []
        for tri_code in tri_codes:
            roster_data = await fetch_and_clean_team_roster(tri_code, "current")
            if roster_data:
                for player in roster_data:
                    await upsert_scraped_player(db, player, tri_code)
                    players_updated.append(player.id)
                await update_team_roster_last_updated(db, tri_code)
        await set_all_other_players_current_team_tri_code_to_null(db, players_updated)
        
async def fetch_current_schedules_for_all_teams():
    async with AsyncSessionLocal() as db:
        tri_codes = await get_all_tri_codes_in_db(db)
        for tri_code in tri_codes:
            current_marked_upcoming_date = await get_date_most_recent_game_marked_as_future(db, tri_code)
            # only fetch and update if current time(UTC) more recent
            current_time = datetime.datetime.now(datetime.timezone.utc)
            if current_marked_upcoming_date is None or current_time >= current_marked_upcoming_date:
                schedule_data = await fetch_and_clean_team_schedule(tri_code, "now")
                if schedule_data:
                    # remove all games in database for this team that are in the future
                    await delete_games_for_team_in_the_future(db, tri_code)
                    # upsert all games
                    await upsert_scraped_games_from_schedule(db, schedule_data)

async def fetch_all_season_schedules_for_all_teams():
    async with AsyncSessionLocal() as db:
        tri_codes = await get_all_tri_codes_in_db(db)
        for season in ["20202021", "20212022", "20222023", "20232024", "20242025", "now"]:
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
            if schedule_data_to_add:
                await upsert_scraped_games_from_schedule(db, schedule_data_to_add)

async def update_daily_features():
    async with AsyncSessionLocal() as db:
        await update_skater_game_features(db)
        await update_goalie_game_features(db)

async def scrape_all_player_logs(seasons:list[int]):
    async with AsyncSessionLocal() as db:
        for season in seasons:
            all_skaters = scrape_all_skater_game_logs(season)
            if all_skaters:
                # get unique player ids
                player_ids = [skater.player_id for skater in all_skaters]
                unique_player_ids = list(set(player_ids))
                missing_players = await get_players_not_in_db(db, unique_player_ids)
                for player in missing_players:
                    player_info = await fetch_and_get_players_info(player)
                    if player_info:
                        await upsert_scraped_player(db, player_info, None)
                    else:
                        # remove from all_skaters
                        all_skaters = [skater for skater in all_skaters if skater.player_id != player]
                await upsert_scraped_game_logs(db, all_skaters)
            all_goalies = scrape_all_goalie_game_logs(season) 
            if all_goalies:
                player_ids = [goalie.player_id for goalie in all_goalies]
                unique_player_ids = list(set(player_ids))
                missing_players = await get_players_not_in_db(db, unique_player_ids)
                for player in missing_players:
                    player_info = await fetch_and_get_players_info(player)
                    if player_info:
                        await upsert_scraped_player(db, player_info, None)
                    else:
                        # remove from all_goalies
                        all_goalies = [goalie for goalie in all_goalies if goalie.player_id != player]
                await upsert_scraped_goalie_game_logs(db, all_goalies)

async def fetch_current_scores():
    async with AsyncSessionLocal() as db:
        scores = await get_current_scores()
        await upsert_scraped_games_from_schedule(db, scores)
