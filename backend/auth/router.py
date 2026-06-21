from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database import get_db
from auth.service import AuthService
from users.schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    result = await auth_service.register_user(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        org_name=user_data.org_name
    )
    return result

@router.post("/login")
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.login_user(login_data.email, login_data.password)

from dependencies import get_current_user
from organizations.service import OrganizationService

@router.get("/me")
async def get_me(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    org_service = OrganizationService(db)
    orgs = await org_service.get_user_organizations(current_user.id)
    org = orgs[0] if orgs else None
    return {
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_superadmin": current_user.is_superadmin
        },
        "org": {
            "id": str(org.id) if org else "",
            "name": org.name if org else ""
        }
    }

@router.post("/refresh")
async def refresh(refresh_data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.refresh_tokens(refresh_data.refresh_token)

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
