from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from .routers import teams_router
from .database import AsyncSessionLocal
from .schedules import add_current_teams_to_db, add_old_teams_to_db, fetch_current_rosters_for_all_teams

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Postgres")
    
    async with AsyncSessionLocal() as db:
        await add_current_teams_to_db(db)
        await add_old_teams_to_db(db)
        await fetch_current_rosters_for_all_teams(db)


    yield 
    
    print("Closing Scheduler and Postgres connection")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(teams_router.router)

@app.get("/")
async def test():
    return {"message": "API working"}
    

