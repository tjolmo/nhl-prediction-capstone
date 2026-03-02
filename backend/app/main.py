from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine
from .routers import teams_router, player_router
from .database import AsyncSessionLocal
from .schedules import (add_current_teams_to_db, add_old_teams_to_db, fetch_current_rosters_for_all_teams, 
                        fetch_current_schedules_for_all_teams, fetch_all_season_schedules_for_all_teams, 
                        fetch_all_player_game_logs, fetch_recent_player_game_logs)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Postgres")
    
    async with AsyncSessionLocal() as db:
        await add_current_teams_to_db(db)
        await add_old_teams_to_db(db)
        await fetch_current_schedules_for_all_teams(db)
        #await fetch_current_rosters_for_all_teams(db)
        #await fetch_all_seasons_schedules_for_all_teams(db)
        #await fetch_all_player_game_logs(db, "all")
        #await fetch_recent_player_game_logs(db, "all")


    yield 
    
    print("Closing Scheduler and Postgres connection")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(teams_router.router)
app.include_router(player_router.router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
),

@app.get("/")
async def test():
    return {"message": "API working"}
    

