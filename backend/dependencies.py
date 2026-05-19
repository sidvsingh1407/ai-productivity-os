from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.jwt_utils import decode_token
from users.service import UserService
from organizations.service import OrganizationService
from models.user import User
from models.organization import Organization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

async def get_current_org(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Organization:
    org_service = OrganizationService(db)
    orgs = await org_service.get_user_organizations(current_user.id)
    if not orgs:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not belong to any organization")
    return orgs[0] # Simplest approach: active org is the first one

def require_role(required_role: str):
    async def role_checker(
        current_user: User = Depends(get_current_user),
        current_org: Organization = Depends(get_current_org),
        db: AsyncSession = Depends(get_db)
    ):
        org_service = OrganizationService(db)
        member = await org_service.get_member(current_org.id, current_user.id)
        if not member or member.role.value != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return current_user
    return role_checker
