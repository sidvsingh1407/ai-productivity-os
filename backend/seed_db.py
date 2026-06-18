import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from database import Base, engine, async_session_maker
from models.user import User
from models.organization import Organization, OrgMember
import uuid
from sqlalchemy.future import select

# Temporary deterministic IDs
TEMP_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
TEMP_ORG_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        # Check if development org exists
        stmt_org = select(Organization).where(Organization.id == TEMP_ORG_ID)
        result_org = await session.execute(stmt_org)
        org = result_org.scalar_one_or_none()

        if not org:
            org = Organization(id=TEMP_ORG_ID, name="Development Organization")
            session.add(org)
            await session.flush()

        # Check if development user exists
        stmt_user = select(User).where(User.id == TEMP_USER_ID)
        result_user = await session.execute(stmt_user)
        user = result_user.scalar_one_or_none()

        if not user:
            user = User(
                id=TEMP_USER_ID,
                email="development@tarkax.com",
                hashed_password="development_mode_no_auth",
                is_active=True,
                is_superadmin=True,
                full_name="Development Mode"
            )
            session.add(user)
            await session.flush()

        # Check if member relation exists
        stmt_member = select(OrgMember).where(OrgMember.user_id == TEMP_USER_ID, OrgMember.org_id == TEMP_ORG_ID)
        result_member = await session.execute(stmt_member)
        member = result_member.scalar_one_or_none()

        if not member:
            member = OrgMember(user_id=TEMP_USER_ID, org_id=TEMP_ORG_ID, role="admin")
            session.add(member)

        await session.commit()
        print("Database seeded with development user.")

if __name__ == "__main__":
    asyncio.run(seed())
