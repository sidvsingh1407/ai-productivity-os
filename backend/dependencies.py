import uuid
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt

from database import get_db
from config import settings
from models.user import User
from models.organization import Organization, OrgMember

# Token format: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # check token type
        token_type: str = payload.get("type", "access")
        if token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise credentials_exception

    stmt = select(User).where(User.id == user_uuid, User.is_active == True)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user

async def get_current_org(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Organization:
    # Get first active organization the user is a member of
    stmt = (
        select(Organization)
        .join(OrgMember)
        .where(OrgMember.user_id == user.id)
        .limit(1)
    )
    result = await db.execute(stmt)
    org = result.scalars().first()

    if org is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found for user"
        )

    return org
