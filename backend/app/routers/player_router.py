from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from app.schemas.teams import TeamInfoOut
from app.crud.players import get_player_by_id
from app.crud.skater_game_logs import upsert_scraped_game_log
from external.moneypuck.player import scrape_skater_game_data

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/add/game_logs/{player_id}", status_code=200)
async def add_player_game_logs(player_id: int, db = Depends(get_db)):
    player_exists = await get_player_by_id(db, player_id)
    if not player_exists:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found in DB")
    game_logs = scrape_skater_game_data(player_id)
    if game_logs:
        num_game_logs_added = 0
        for game_log in game_logs:
            await upsert_scraped_game_log(db, game_log)
            num_game_logs_added += 1
        return {"player_id": player_id, "game_logs_added": num_game_logs_added}
    raise HTTPException(status_code=404, detail=f"Game logs for player {player_id} not found in external API")