from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
import uuid
from uuid import UUID
from typing import Optional

from config import settings
from auth.token_repository import TokenRepository

class TokenService:
    def __init__(self, repository: Optional[TokenRepository] = None):
        self.repository = repository

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        """Creates a JWT access token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def create_refresh_token(self, user_id: UUID, expires_days: int = 30) -> str:
        """Creates a JWT refresh token with a JTI and stores the JTI hash in the DB."""
        jti = str(uuid.uuid4())
        expire = datetime.now(timezone.utc) + timedelta(days=expires_days)

        to_encode = {
            "sub": str(user_id),
            "jti": jti,
            "type": "refresh",
            "exp": expire
        }

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        if self.repository:
            await self.repository.store_jti_hash(user_id, jti, expiry_days=expires_days)

        return encoded_jwt

    async def verify_refresh_token(self, token: str) -> dict:
        """Decodes and validates a JWT refresh token against signature, expiration, and DB state."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

            jti = payload.get("jti")
            if not jti:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing JTI in token")

            if self.repository:
                user_token = await self.repository.get_refresh_token_by_jti(jti)
                if not user_token:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked or invalid")

            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def verify_token(self, token: str) -> dict:
        """Decodes and validates a generic JWT token statelessly (useful for access tokens)."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def create_verification_token(self, user_id: UUID) -> str:
        """Creates an email verification token using TokenRepository."""
        if not self.repository:
            raise ValueError("TokenRepository is required")
        return await self.repository.create_token(user_id, "EMAIL_VERIFICATION", expiry_hours=24)

    async def create_password_reset_token(self, user_id: UUID) -> str:
        """Creates a password reset token using TokenRepository."""
        if not self.repository:
            raise ValueError("TokenRepository is required")
        return await self.repository.create_token(user_id, "PASSWORD_RESET", expiry_hours=1)

    async def revoke_refresh_tokens(self, user_id: UUID) -> None:
        """Revokes all refresh tokens for a user."""
        if self.repository:
            await self.repository.revoke_user_refresh_tokens(user_id)

    async def revoke_single_refresh_token(self, jti: str) -> None:
        """Revokes a specific refresh token by its JTI."""
        if self.repository:
            await self.repository.revoke_refresh_token_by_jti(jti)