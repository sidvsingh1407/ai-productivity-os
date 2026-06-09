from pydantic import BaseModel, ConfigDict, EmailStr, Field
from users.schemas import UserResponse
from organizations.schemas import OrgResponse

class AuthResponse(BaseModel):
    user: UserResponse
    org: OrgResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)

class VerifyEmailRequest(BaseModel):
    token: str

class ResendVerificationRequest(BaseModel):
    email: EmailStr

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)
