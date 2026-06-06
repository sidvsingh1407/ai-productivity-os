import secrets
import hashlib
import uuid
from datetime import datetime
from typing import Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.api_platform import ApiKey, ApiTier

# Redis integration for rate limiting
import redis.asyncio as redis
from config import settings

# Initialize redis connection lazily
redis_client = None

def get_redis_client():
    global redis_client
    if not redis_client:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return redis_client

class ApiKeyService:
    @staticmethod
    def generate_key(is_test: bool = False) -> str:
        """Generates a secure, high-entropy API key."""
        prefix = "tkx_test_" if is_test else "tkx_live_"
        random_bytes = secrets.token_hex(24) # 48 chars
        return f"{prefix}{random_bytes}"

    @staticmethod
    def hash_key(raw_key: str) -> str:
        """Hashes the raw API key using SHA-256."""
        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()

    @staticmethod
    async def create_api_key(
        db: AsyncSession,
        organization_id: uuid.UUID,
        name: str,
        tier: ApiTier = ApiTier.free,
        is_test: bool = False,
        expires_at: Optional[datetime] = None
    ) -> Tuple[ApiKey, str]:
        """Creates a new API key for an organization. Returns the model and the raw key."""
        raw_key = ApiKeyService.generate_key(is_test)
        hashed_key = ApiKeyService.hash_key(raw_key)

        api_key = ApiKey(
            organization_id=organization_id,
            name=name,
            key_hash=hashed_key,
            tier=tier,
            expires_at=expires_at,
            is_active=True
        )

        db.add(api_key)
        await db.commit()
        await db.refresh(api_key)

        return api_key, raw_key

    @staticmethod
    async def validate_key(db: AsyncSession, raw_key: str) -> Optional[ApiKey]:
        """Validates an API key and updates its last_used_at timestamp."""
        hashed_key = ApiKeyService.hash_key(raw_key)

        query = select(ApiKey).where(ApiKey.key_hash == hashed_key)
        result = await db.execute(query)
        api_key = result.scalar_one_or_none()

        if not api_key:
            return None

        if not api_key.is_active:
            # We explicitly check this in dependencies to return 403, so return it here to allow check
            return api_key

        if api_key.expires_at and api_key.expires_at < datetime.now(api_key.expires_at.tzinfo):
            return None

        return api_key

    @staticmethod
    async def update_last_used(db: AsyncSession, api_key_id: uuid.UUID) -> None:
        """Update last_used_at for an API key."""
        query = select(ApiKey).where(ApiKey.id == api_key_id)
        result = await db.execute(query)
        api_key = result.scalar_one_or_none()
        if api_key:
            # We don't want to use timezone aware now, we use func.now() usually but this is simpler
            # Update last used without blocking the request too much
            api_key.last_used_at = datetime.utcnow()
            db.add(api_key)
            await db.commit()

    @staticmethod
    async def revoke_key(db: AsyncSession, api_key_id: uuid.UUID) -> bool:
        """Revokes an API key by setting is_active to False."""
        query = select(ApiKey).where(ApiKey.id == api_key_id)
        result = await db.execute(query)
        api_key = result.scalar_one_or_none()

        if not api_key:
            return False

        api_key.is_active = False
        db.add(api_key)
        await db.commit()
        return True

class RateLimitService:
    TIER_LIMITS = {
        ApiTier.free: 100,
        ApiTier.pro: 5000,
        ApiTier.enterprise: float('inf') # Custom limits handled manually or via db if needed, but float inf for now
    }

    @staticmethod
    async def check_rate_limit(api_key_id: uuid.UUID, tier: ApiTier) -> bool:
        """
        Enforces server-side rate limiting using Redis.
        Returns True if the request is allowed, False if rate limited.
        """
        limit = RateLimitService.TIER_LIMITS.get(tier, 100)

        if limit == float('inf'):
            return True

        client = get_redis_client()

        # Current date for daily limit
        today_str = datetime.utcnow().strftime('%Y-%m-%d')
        redis_key = f"rate_limit:{api_key_id}:{today_str}"

        # Pipeline for atomic operations
        try:
            async with client.pipeline(transaction=True) as pipe:
                pipe.incr(redis_key)
                pipe.expire(redis_key, 86400) # 24 hours
                results = await pipe.execute()

            current_count = results[0]

            return current_count <= limit
        except Exception as e:
            # In case redis is down, fallback gracefully to allow or block based on strictness.
            # We allow it to prevent total outage if redis drops.
            print(f"Redis rate limiting error: {e}")
            return True
