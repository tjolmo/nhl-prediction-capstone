from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os

engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)