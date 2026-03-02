import datetime

from fastapi import APIRouter, Depends, HTTPException
from app.crud.games import get_next_game_info_by_tri_code
from app.dependencies import get_db
from app.schemas.player import GoalieLast5BasicStatsGetOut, GoalieSeasonBasicStatsGetOut, PlayerGameLogAddOut, PlayerGameLogGetOut, GoalieGameLogGetOut, PlayerNextGameGetOut, SkaterLast5BasicStatsGetOut, SkaterSeasonBasicStatsGetOut, PlayerBasicInfoOut
from app.crud.players import get_skater_by_id, update_player_game_log_last_updated, get_goalie_by_id, get_player_by_id
from app.crud.skater_game_logs import get_skater_last_5_basic_stats_from_db, upsert_scraped_game_logs, get_player_game_log_by_game_and_player_id, get_skater_season_basic_stats_from_db
from app.crud.goalie_game_logs import get_goalie_last_5_basic_stats_from_db, get_goalie_season_basic_stats_from_db, upsert_scraped_goalie_game_logs
from external.moneypuck.player import scrape_skater_game_data, scrape_goalie_game_data
from external.nhl.games import fetch_and_get_players_in_a_game

router = APIRouter(prefix="/players", tags=["players"])

async def add_skater_game_logs(player_id: int, db = Depends(get_db)):
    """Adds scraped player game logs to DB for a given player ID. Three seasons default"""
    player_exists = await get_skater_by_id(db, player_id)
    if not player_exists:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found in DB or is a goalie")
    game_logs = scrape_skater_game_data(player_id)
    if game_logs:
        num_game_logs_added = 0
        for game_log in game_logs:
            await upsert_scraped_game_logs(db, [game_log])
            num_game_logs_added += 1
        await update_player_game_log_last_updated(db, player_id)
        return PlayerGameLogAddOut(player_id=player_id, game_logs_added=num_game_logs_added)
    raise HTTPException(status_code=404, detail=f"Game logs for player {player_id} not found in external API")

@router.post("/add/goalie/game_logs/{player_id}", status_code=200, response_model=PlayerGameLogAddOut)
async def add_goalie_game_logs(player_id: int, db = Depends(get_db)):
    """Adds scraped player game logs to DB for a given player ID. Three seasons default"""
    player_exists = await get_goalie_by_id(db, player_id)
    if not player_exists:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found in DB or is not a goalie")
    game_logs = scrape_goalie_game_data(player_id)
    if game_logs:
        num_game_logs_added = 0
        for game_log in game_logs:
            await upsert_scraped_goalie_game_logs(db, game_log)
            num_game_logs_added += 1
        await update_player_game_log_last_updated(db, player_id)
        return PlayerGameLogAddOut(player_id=player_id, game_logs_added=num_game_logs_added)
    raise HTTPException(status_code=404, detail=f"Game logs for player {player_id} not found in external API")

@router.get("/get/skater/game_log/{game_id}/{player_id}", status_code=200, response_model=PlayerGameLogGetOut)
async def get_skater_game_log(game_id: int, player_id: int, db = Depends(get_db)):
    """Fetches a specific game log for a given player ID and game ID."""
    try:
        game_log = await get_player_game_log_by_game_and_player_id(db, game_id, player_id)
        if game_log:
            return game_log
        else:
            raise HTTPException(status_code=404, detail=f"Game log for player {player_id} and game {game_id} not found in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving game log for player {player_id} and game {game_id} from DB: {e}")

@router.get("/get/goalie/game_log/{game_id}/{player_id}", status_code=200, response_model=GoalieGameLogGetOut)
async def get_player_game_log(game_id: int, player_id: int, db = Depends(get_db)):
    """Fetches a specific game log for a given player ID and game ID."""
    try:
        game_log = await get_player_game_log_by_game_and_player_id(db, game_id, player_id)
        if game_log:
            return game_log
        else:
            raise HTTPException(status_code=404, detail=f"Game log for goalie {player_id} and game {game_id} not found in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving game log for goalie {player_id} and game {game_id} from DB: {e}")

@router.get("/skater/{player_id}/basic_stats/{season}", status_code=200, response_model=SkaterSeasonBasicStatsGetOut)
async def get_skater_season_basic_stats(player_id: int, season: int, db = Depends(get_db)):
    """Fetches basic season stats for a skater by player ID and season."""
    try:
        stats = await get_skater_season_basic_stats_from_db(db, player_id, season)
        if stats:
            return SkaterSeasonBasicStatsGetOut(games=stats["games"], goals=stats["goals"], assists=stats["assists"], points=stats["points"])
        else:
            raise HTTPException(status_code=404, detail=f"Season {season} stats for skater {player_id} not found in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving season {season} stats for skater {player_id} from DB: {e}")

@router.get("/skater/{player_id}/last_5/basic_stats", status_code=200, response_model=list[SkaterLast5BasicStatsGetOut])
async def get_skater_last_5_basic_stats(player_id: int, db = Depends(get_db)):
    """Fetches basic stats for a skater's last 5 games by player ID."""
    try:
        stats = await get_skater_last_5_basic_stats_from_db(db, player_id)
        if stats:
            return [SkaterLast5BasicStatsGetOut(
                date=datetime.datetime.strptime(str(stat["game_date"]), "%Y%m%d").strftime("%b %d") if stat["game_date"] else None,
                opposing_team_tricode=stat["opposing_team_tricode"],
                goals=stat["goals"],
                assists=stat["assists"],
                points=stat["points"],
                home_away=stat["home_away"]
            ) for stat in stats]
        else:
            raise HTTPException(status_code=404, detail=f"Last 5 games stats for skater {player_id} not found in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving last 5 games stats for skater {player_id} from DB: {e}")

@router.get("/player/{player_id}/basic_data", status_code=200, response_model=PlayerBasicInfoOut)
async def get_player_data(player_id: int, db = Depends(get_db)):
    """Fetches basic info for a player by player ID."""
    player_info = await get_player_by_id(db, player_id)
    if not player_info:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found in DB")
    return PlayerBasicInfoOut(
        name = f"{player_info.first_name} {player_info.last_name}",
        number=player_info.number,
        position=player_info.position,
        team=player_info.current_team_tri_code,
        headshotUrl=player_info.headshot
    )

@router.get("/player/{player_id}/upcoming_game", status_code=200, response_model=PlayerNextGameGetOut)
async def get_player_upcoming_game(player_id: int, db = Depends(get_db)):
    """Fetches upcoming game info for a player by player ID."""
    player_info = await get_player_by_id(db, player_id)
    if not player_info:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found in DB")
    if player_info.current_team_tri_code is None:
        raise HTTPException(status_code=404, detail=f"Player {player_id} does not have a current team in DB")
    upcoming_game = await get_next_game_info_by_tri_code(db, player_info.current_team_tri_code)
    if not upcoming_game:
        raise HTTPException(status_code=404, detail=f"Upcoming game for player {player_id} not found in DB")
    return PlayerNextGameGetOut(
        # int to string from YYYYMMDD to Month Name Day, Year
        date = datetime.datetime.strptime(str(upcoming_game.date), "%Y%m%d").strftime("%B %d, %Y") if upcoming_game.date else None,
        opposing_team_tricode=upcoming_game.away_team_tri_code if upcoming_game.home_team_tri_code == player_info.current_team_tri_code else upcoming_game.home_team_tri_code,
        venue=upcoming_game.venue,
        time=upcoming_game.start_time,
        home_away="HOME" if upcoming_game.home_team_tri_code == player_info.current_team_tri_code else "AWAY"
    )

@router.get("/goalie/{player_id}/last_5/basic_stats", status_code=200, response_model=list[GoalieLast5BasicStatsGetOut])
async def get_goalie_last_5_basic_stats(player_id: int, db = Depends(get_db)):
    """Fetches basic stats for a goalie's last 5 games by player ID."""
    try:
        stats = await get_goalie_last_5_basic_stats_from_db(db, player_id)
        if stats:
            return [GoalieLast5BasicStatsGetOut(
                date=datetime.datetime.strptime(str(stat["date"]), "%Y%m%d").strftime("%b %d") if stat["date"] else None,
                opposing_team_tricode=stat["opposing_team_tricode"],
                saves=stat["saves"],
                goals_against=stat["goals_against"],
                save_percentage=round(stat["save_percentage"], 3) if stat["save_percentage"] is not None else None,
                home_away=stat["home_away"]
            ) for stat in stats]
        else:
            raise HTTPException(status_code=404, detail=f"Last 5 games stats for goalie {player_id} not found in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving last 5 games stats for goalie {player_id} from DB: {e}")

@router.get("/goalie/{player_id}/basic_stats/{season}", status_code=200, response_model=GoalieSeasonBasicStatsGetOut)
async def get_goalie_season_basic_stats(player_id: int, season: int, db = Depends(get_db)):
    """Fetches basic season stats for a goalie by player ID and season."""
    try:
        stats = await get_goalie_season_basic_stats_from_db(db, player_id, season)
        if stats:
            return GoalieSeasonBasicStatsGetOut(
                games=stats["games"], 
                gaa=round(stats["gaa"], 3) if stats["gaa"] is not None else None, save_percentage=round(stats["save_percentage"], 3) if stats["save_percentage"] is not None else None)
        else:
            raise HTTPException(status_code=404, detail=f"Season {season} stats for goalie {player_id} not found in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving season {season} stats for goalie {player_id} from DB: {e}")