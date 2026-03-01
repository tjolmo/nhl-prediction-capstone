from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from .routers import teams_router, player_router
from .database import AsyncSessionLocal
from .schedules import (add_current_teams_to_db, add_old_teams_to_db, fetch_current_rosters_for_all_teams, 
                        fetch_current_schedules_for_all_teams, fetch_past_two_seasons_schedules_for_all_teams, 
                        fetch_all_skater_game_logs, fetch_recent_skater_game_logs,
                        fetch_goalie_all_game_logs_for_recent_games)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Postgres")
    
    async with AsyncSessionLocal() as db:
        await add_current_teams_to_db(db)
        await add_old_teams_to_db(db)
        await fetch_current_schedules_for_all_teams(db)
        #await fetch_past_two_seasons_schedules_for_all_teams(db)
        await fetch_current_rosters_for_all_teams(db)
        #await fetch_all_skater_game_logs(db)
        await fetch_recent_skater_game_logs(db)
        #await fetch_skater_all_game_logs_for_recent_games(db)
        #await fetch_goalie_all_game_logs_for_recent_games(db)


    yield 
    
    print("Closing Scheduler and Postgres connection")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(teams_router.router)
app.include_router(player_router.router)

@app.get("/")
async def test():
    return {"message": "API working"}
    

