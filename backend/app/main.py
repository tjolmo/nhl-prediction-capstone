from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from .routers import teams_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Postgres")
    yield 
    print("Closing Postgres connection")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(teams_router.router)

@app.get("/")
async def test():
    return {"message": "API working"}
    

