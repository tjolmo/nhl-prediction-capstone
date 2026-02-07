from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Postgres")
    yield 
    print("Closing Postgres connection")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def test():
    return {"message": "API working"}
    