from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import settings

database_url = settings.DATABASE_URL

if database_url:
    database_url = database_url.replace("postgres://", "postgresql://")
    
    if "postgresql://" in database_url and "+asyncpg" not in database_url:
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

engine_kwargs = {
    "echo": False,
    "pool_pre_ping": True,
}

if "sqlite" not in database_url:
    engine_kwargs["pool_size"] = 20
    engine_kwargs["max_overflow"] = 0

engine = create_async_engine(
    database_url,
    **engine_kwargs
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
