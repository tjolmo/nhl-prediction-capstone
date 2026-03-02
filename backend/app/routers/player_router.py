from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from app.schemas.player import PlayerGameLogAddOut, PlayerGameLogGetOut, GoalieGameLogGetOut, SkaterLast5BasicStatsGetOut, SkaterSeasonBasicStatsGetOut
from app.crud.players import get_skater_by_id, update_player_game_log_last_updated, get_goalie_by_id
from app.crud.skater_game_logs import get_skater_last_5_basic_stats_from_db, upsert_scraped_game_logs, get_player_game_log_by_game_and_player_id, get_skater_season_basic_stats_from_db
from app.crud.goalie_game_logs import upsert_scraped_goalie_game_logs
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
                date=stat["game_date"],
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