import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///local_test.db"

from main import app
from database import Base, engine, async_session_maker
from models.user import User
from models.organization import Organization
from auth.password_utils import hash_password

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        # Check if users already exist
        org = Organization(name="Test Org")
        session.add(org)
        await session.flush()

        superadmin = User(
            email="superadmin@tarkax.com",
            hashed_password=hash_password("password123"),
            is_active=True,
            is_superadmin=True, full_name="Super Admin"
        )
        user = User(
            email="user@tarkax.com",
            hashed_password=hash_password("password123"),
            is_active=True,
            is_superadmin=False, full_name="Standard User"
        )
        session.add(superadmin)
        session.add(user)
        await session.commit()
        print("Database seeded with test users.")

if __name__ == "__main__":
    asyncio.run(seed())
