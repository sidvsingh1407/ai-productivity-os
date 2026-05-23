from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import async_session_maker
from config import settings
from models.user import User
from models.organization import Organization, OrgMember

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]) # default algorithm as settings does not have it yet
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user

async def get_current_org(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Organization:
    stmt = select(Organization).join(OrgMember).where(OrgMember.user_id == current_user.id)
    result = await db.execute(stmt)
    org = result.scalar_one_or_none()

    if org is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not belong to an organization"
        )

    return org

def require_role(required_role: str):
    async def role_checker(current_user: User = Depends(get_current_user)):
        # Very basic role check for placeholder purposes
        return current_user
    return role_checker

async def require_superadmin(current_user: User = Depends(get_current_user)):
    if getattr(current_user, 'is_superadmin', False) != True:
        raise HTTPException(status_code=403, detail="Superadmin access required")
    return current_user
