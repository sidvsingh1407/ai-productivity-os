import uuid
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import async_session_maker
from models.user import User
from models.organization import Organization, OrgMember

# Temporary deterministic IDs
TEMP_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
TEMP_ORG_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    stmt = select(User).where(User.id == TEMP_USER_ID)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        # Fallback if DB seed somehow hasn't run yet
        return User(
            id=TEMP_USER_ID,
            email="development@tarkax.com",
            full_name="Development Mode",
            is_superadmin=True,
            is_active=True
        )
    return user

async def get_current_org(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Organization:
    stmt = select(Organization).where(Organization.id == TEMP_ORG_ID)
    result = await db.execute(stmt)
    org = result.scalar_one_or_none()

    if org is None:
        return Organization(
            id=TEMP_ORG_ID,
            name="Development Organization",
            slug="development-organization"
        )
    return org

ROLE_HIERARCHY = {
    "owner": 4,
    "admin": 3,
    "member": 2,
    "viewer": 1
}

def require_role(required_role: str):
    async def role_checker(
        current_user: User = Depends(get_current_user),
        current_org: Organization = Depends(get_current_org),
        db: AsyncSession = Depends(get_db)
    ):
        return current_user
    return role_checker

async def require_superadmin(current_user: User = Depends(get_current_user)):
    return current_user
