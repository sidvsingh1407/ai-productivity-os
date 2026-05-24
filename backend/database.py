from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Setup async engine
database_url = settings.DATABASE_URL.replace('postgres://', 'postgresql://') if settings.DATABASE_URL else 'sqlite+aiosqlite:///./test.db'
engine = create_async_engine(
    database_url,
    echo=False,
)

# Setup async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base declarative model class
class Base(DeclarativeBase):
    pass

# Dependency to yield database sessions
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
git add .
git commit -m "fix: complete deployment configuration - prompts 1-6"
git push origin main
