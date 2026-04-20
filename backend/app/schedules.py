from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, insert, not_, exists
from .models import SkaterGameLog, GoalieGameLog, SkaterGameFeatures, GoalieGameFeatures
from external.nhl.players import fetch_and_get_players_info
from .crud.goalie_game_logs import get_goalie_most_recent_game_date_and_last_updated
from external.nhl.teams import fetch_and_clean_team, fetch_and_clean_team_roster, fetch_and_clean_team_schedule
from external.nhl.games import fetch_and_get_players_in_a_game
from external.moneypuck.player import scrape_skater_game_data, scrape_goalie_game_data
from .crud.team_history import upsert_team_history, check_team_history_exists_and_updated
from .crud.teams import get_all_tri_codes_in_db, upsert_team,update_team_roster_last_updated, get_all_tri_codes_update_roster
from .crud.games import check_if_games_in_db, get_all_teams_most_recent_game_dates, upsert_scraped_games_from_schedule, get_date_most_recent_game_marked_as_future
from .crud.players import get_all_goalie_ids_and_teams, get_all_skater_ids_and_teams, get_all_skaters_on_a_roster, get_players_not_in_db, upsert_scraped_player, set_all_other_players_current_team_tri_code_to_null, get_all_goalies_on_a_roster
from .crud.skater_game_logs import get_player_most_recent_game_date_and_last_updated, upsert_scraped_game_logs
from .crud.goalie_game_logs import upsert_scraped_goalie_game_logs
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
        
async def fetch_current_schedules_for_all_teams(db: AsyncSession):
    tri_codes = await get_all_tri_codes_in_db(db)
    for tri_code in tri_codes:
        current_marked_upcoming_date = await get_date_most_recent_game_marked_as_future(db, tri_code)
        # only fetch and update if current time(UTC) more recent
        current_time = datetime.datetime.now(datetime.timezone.utc)
        if current_marked_upcoming_date is None or current_time >= current_marked_upcoming_date:
            schedule_data = await fetch_and_clean_team_schedule(tri_code, "now")
            if schedule_data:
                await upsert_scraped_games_from_schedule(db, schedule_data)

async def fetch_all_season_schedules_for_all_teams(db: AsyncSession):
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

async def fetch_all_player_game_logs(db: AsyncSession, player_type: str = "all"):
    """Fetches and upserts player game logs for all games"""
    if player_type not in ["all", "skater", "goalie"]:
        raise ValueError("Invalid player type. Must be 'all', 'skater', or 'goalie'.")

    game_logs = None
    if player_type in ["all", "skater"]:    
        players = await get_all_skater_ids_and_teams(db)
        for player in players:
            game_logs = scrape_skater_game_data(player[0])
            #upsert to db
            if game_logs:
                await upsert_scraped_game_logs(db, game_logs)
    game_logs = None
    if player_type in ["all", "goalie"]:
        players = await get_all_goalie_ids_and_teams(db)
        for player in players:
            game_logs = scrape_goalie_game_data(player[0])
            #upsert to db
            if game_logs:
                await upsert_scraped_goalie_game_logs(db, game_logs)
    
async def fetch_recent_player_game_logs(db: AsyncSession, player_type: str = "all"):
    """Fetches and upserts player game logs for recent games for a team by tri code."""
    if player_type not in ["all", "skater", "goalie"]:
        raise ValueError("Invalid player type. Must be 'all', 'skater', or 'goalie'.")
    
    #get all teams most recent game date played
    most_recent_games_team_int = await get_all_teams_most_recent_game_dates(db)
    most_recent_games_team_dt = {}
    #modify to datetime with utc timezone 
    for tri_code, game_date in most_recent_games_team_int.items():
        try: 
            datetime_game_date = datetime.datetime.strptime(str(game_date), "%Y%m%d").replace(tzinfo=datetime.timezone.utc)
            most_recent_games_team_dt[tri_code] = datetime_game_date
        except Exception as e:
            print(f"Error converting game date for team {tri_code}: {e}")
            most_recent_games_team_dt[tri_code] = None

    game_logs = None
    if player_type in ["all", "skater"]:
        players = await get_all_skaters_on_a_roster(db)
        for player in players:
            player_id = player[0]
            tri_code = player[1]
            latest_game_int = most_recent_games_team_int.get(tri_code)
            latest_game_datetime = most_recent_games_team_dt.get(tri_code)

            skater_info = await get_player_most_recent_game_date_and_last_updated(db, player_id)
            if skater_info:
                latest_game_log_date = skater_info[0]
                last_updated = skater_info[1]

                if latest_game_int and \
                    (latest_game_int > latest_game_log_date) and \
                    (latest_game_datetime > last_updated):
                    # scrape just recent logs
                    game_logs = scrape_skater_game_data(player_id, latest_game_int)

            else:
                #scrape all if player has no game logs in db
                game_logs = scrape_skater_game_data(player_id)

            #upsert to db
            if game_logs:
                await upsert_scraped_game_logs(db, game_logs)

    game_logs = None
    if player_type in ["all", "goalie"]:
        players = await get_all_goalies_on_a_roster(db)
        for player in players:
            player_id = player[0]
            tri_code = player[1]
            latest_game_int = most_recent_games_team_int.get(tri_code)
            latest_game_datetime = most_recent_games_team_dt.get(tri_code)

            goalie_info = await get_goalie_most_recent_game_date_and_last_updated(db, player_id)
            if goalie_info:
                latest_game_log_date = goalie_info[0]
                last_updated = goalie_info[1]

                if latest_game_int and \
                    (latest_game_int > latest_game_log_date) and \
                    (latest_game_datetime > last_updated):
                    # scrape just recent logs
                    game_logs = scrape_goalie_game_data(player_id, latest_game_int)

            else:
                #scrape all if player has no game logs in db
                game_logs = scrape_goalie_game_data(player_id)

            #upsert to db
            if game_logs:
                await upsert_scraped_goalie_game_logs(db, game_logs)

async def update_daily_features(session: AsyncSession) -> None:
    #skater portion
    skater_window_query = select(
        SkaterGameLog.game_id,
        SkaterGameLog.player_id,
        func.avg(SkaterGameLog.x_goals).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_goals"),
        func.avg(SkaterGameLog.toi).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_toi"),
        func.avg(SkaterGameLog.game_score).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_game_score"),
        func.avg(SkaterGameLog.shot_attempts).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_shot_attempts"),
        func.avg(SkaterGameLog.high_danger_shots).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_high_danger_shots"),
        func.avg(SkaterGameLog.on_ice_x_goals_percentage).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_on_ice_x_goals_percentage"),
        func.avg(SkaterGameLog.primary_assists).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_primary_assists"),
        func.avg(SkaterGameLog.goals).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_goals"),
        func.avg(SkaterGameLog.points).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_points")
    ).where(
        not_(
            exists().where(
                (SkaterGameFeatures.game_id == SkaterGameLog.game_id) &
                (SkaterGameFeatures.player_id == SkaterGameLog.player_id)
            )
        )
    )
    # Filter out None values
    new_skater_features = [row for row in (await session.execute(skater_window_query)).mappings().all() if row["rolling_x_goals"] is not None]
    if new_skater_features:
        await session.execute(insert(SkaterGameFeatures), new_skater_features)

    # Goalie portion
    goalie_window_query = select(
        GoalieGameLog.game_id,
        GoalieGameLog.player_id,
        func.avg(GoalieGameLog.x_goals_against).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_goals_against"),
        func.avg(GoalieGameLog.goals_against).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_goals_against"),
        func.avg(GoalieGameLog.sog).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_sog"),
        func.avg(GoalieGameLog.flurry_adjusted_x_goals).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_flurry_adjusted_x_goals"),
        func.avg(GoalieGameLog.high_danger_x_goals).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_high_danger_x_goals"),
        func.avg(GoalieGameLog.x_sog).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_sog"),
        func.avg(GoalieGameLog.high_danger_shots).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_high_danger_shots"),
        func.avg(GoalieGameLog.rebounds).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_rebounds"),
        func.avg(GoalieGameLog.x_rebounds).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_rebounds"),
        func.avg(GoalieGameLog.freeze).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_freeze"),
        func.avg(GoalieGameLog.x_freeze).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_freeze"),
    ).where(
        not_(
            exists().where(
                (GoalieGameFeatures.game_id == GoalieGameLog.game_id) &
                (GoalieGameFeatures.player_id == GoalieGameLog.player_id)
            )
        )
    )
    
    new_goalie_features = [row for row in (await session.execute(goalie_window_query)).mappings().all() if row["rolling_x_goals_against"] is not None]
    if new_goalie_features:
        await session.execute(insert(GoalieGameFeatures), new_goalie_features)

    # Team Portion, Add later
    
    await session.commit()