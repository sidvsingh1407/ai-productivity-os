import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_token import UserToken

class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def hash_token(self, token: str) -> str:
        """Returns the SHA256 hash of a plain token string."""
        return hashlib.sha256(token.encode()).hexdigest()

    async def create_token(self, user_id: UUID, token_type: str, expiry_hours: int = 1) -> str:
        """Generates a secure random token, stores its hash, and returns the raw token."""
        raw_token = secrets.token_urlsafe(32)
        token_hash = self.hash_token(raw_token)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=expiry_hours)

        user_token = UserToken(
            user_id=user_id,
            token_hash=token_hash,
            token_type=token_type,
            expires_at=expires_at
        )
        self.session.add(user_token)
        await self.session.flush()
        return raw_token

    async def store_jti_hash(self, user_id: UUID, jti: str, expiry_days: int = 30) -> None:
        """Stores a SHA256 hash of a JWT JTI to track its revocation status."""
        jti_hash = self.hash_token(jti)
        expires_at = datetime.now(timezone.utc) + timedelta(days=expiry_days)

        user_token = UserToken(
            user_id=user_id,
            token_hash=jti_hash,
            token_type="REFRESH_TOKEN",
            expires_at=expires_at
        )
        self.session.add(user_token)
        await self.session.flush()

    async def get_token(self, token: str, token_type: str) -> Optional[UserToken]:
        """Retrieves a valid, unused token from the database."""
        token_hash = self.hash_token(token)
        stmt = select(UserToken).where(
            UserToken.token_hash == token_hash,
            UserToken.token_type == token_type,
            UserToken.used_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_refresh_token_by_jti(self, jti: str) -> Optional[UserToken]:
        """Retrieves a valid, unrevoked refresh token via its JTI hash."""
        return await self.get_token(jti, "REFRESH_TOKEN")

    async def mark_used(self, user_token: UserToken) -> None:
        """Marks a token as used/revoked."""
        user_token.used_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def revoke_token(self, token: str, token_type: str) -> None:
        """Revokes a token by deleting it or marking it used. For now, mark used."""
        user_token = await self.get_token(token, token_type)
        if user_token:
            user_token.used_at = datetime.now(timezone.utc)
            await self.session.flush()

    async def revoke_refresh_token_by_jti(self, jti: str) -> None:
        """Revokes a refresh token using its JTI."""
        await self.revoke_token(jti, "REFRESH_TOKEN")

    async def revoke_user_refresh_tokens(self, user_id: UUID) -> None:
        """Marks all active refresh tokens for a user as used (effectively revoking them)."""
        stmt = select(UserToken).where(
            UserToken.user_id == user_id,
            UserToken.token_type == "REFRESH_TOKEN",
            UserToken.used_at.is_(None)
        )
        result = await self.session.execute(stmt)
        tokens = result.scalars().all()
        for token in tokens:
            token.used_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def delete_expired(self) -> None:
        """Deletes tokens that have expired."""
        stmt = delete(UserToken).where(UserToken.expires_at < datetime.now(timezone.utc))
        await self.session.execute(stmt)
        await self.session.flush()