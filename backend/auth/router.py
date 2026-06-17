from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database import get_db
from auth.service import AuthService
from users.schemas import UserCreate
from auth.schemas import AuthResponse, RegisterResponse, ForgotPasswordRequest, ResetPasswordRequest, VerifyEmailRequest, ResendVerificationRequest, ChangePasswordRequest
from dependencies import get_current_user
from models.user import User
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
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
async def logout(logout_data: LogoutRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    await auth_service.logout(current_user, logout_data.refresh_token)
    return {"message": "Logged out successfully"}

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    token = await auth_service.forgot_password(request.email)
    # Exposing the reset URL for development/demo purposes because emails are mock.
    reset_url = None
    if token:
        from config import settings
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    return {
        "message": "If an account exists, a password reset link has been sent.",
        "reset_url": reset_url
    }

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    await auth_service.reset_password(request.token, request.new_password)
    return {"message": "Password reset successfully."}

@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(request: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    await auth_service.verify_email(request.token)
    return {"message": "Email verified successfully."}

@router.post("/resend-verification", status_code=status.HTTP_200_OK)
async def resend_verification(request: ResendVerificationRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    await auth_service.resend_verification(request.email)
    return {"message": "Verification email sent if account exists and is unverified."}

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(request: ChangePasswordRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    auth_service = AuthService(db)
    await auth_service.change_password(current_user, request.current_password, request.new_password)
    return {"message": "Password changed successfully."}