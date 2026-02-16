from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from app.schemas.player import PlayerGameLogAddOut, PlayerGameLogGetOut
from app.crud.players import get_player_by_id, update_player_game_log_last_updated
from app.crud.skater_game_logs import upsert_scraped_game_log, get_player_game_log_by_game_and_player_id
from external.moneypuck.player import scrape_skater_game_data

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/add/game_logs/{player_id}", status_code=200, response_model=PlayerGameLogAddOut)
async def add_player_game_logs(player_id: int, db = Depends(get_db)):
    """Adds scraped player game logs to DB for a given player ID. Three seasons default"""
    player_exists = await get_player_by_id(db, player_id)
    if not player_exists:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found in DB")
    game_logs = scrape_skater_game_data(player_id)
    if game_logs:
        num_game_logs_added = 0
        for game_log in game_logs:
            await upsert_scraped_game_log(db, game_log)
            num_game_logs_added += 1
        await update_player_game_log_last_updated(db, player_id)
        return PlayerGameLogAddOut(player_id=player_id, game_logs_added=num_game_logs_added)
    raise HTTPException(status_code=404, detail=f"Game logs for player {player_id} not found in external API")

@router.get("/get/game_log/{game_id}/{player_id}", status_code=200, response_model=PlayerGameLogGetOut)
async def get_player_game_log(game_id: int, player_id: int, db = Depends(get_db)):
    """Fetches a specific game log for a given player ID and game ID."""
    try:
        game_log = await get_player_game_log_by_game_and_player_id(db, game_id, player_id)
        if game_log:
            return game_log
        else:
            raise HTTPException(status_code=404, detail=f"Game log for player {player_id} and game {game_id} not found in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving game log for player {player_id} and game {game_id} from DB: {e}")