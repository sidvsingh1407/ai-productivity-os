from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database import get_db
from auth.service import AuthService
from users.schemas import UserCreate
from auth.schemas import AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    result = await auth_service.register_user(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        org_name=user_data.org_name
    )
    return result

@router.post("/login", response_model=AuthResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.login_user(login_data.email, login_data.password)

@router.post("/refresh")
async def refresh(refresh_data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.refresh_tokens(refresh_data.refresh_token)

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
