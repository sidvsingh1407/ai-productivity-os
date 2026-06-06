from fastapi import Request, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

from .service import ApiKeyService, RateLimitService
from models.api_platform import ApiKey

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(
    request: Request,
    raw_key: str = Depends(api_key_header),
    db: AsyncSession = Depends(get_db)
) -> ApiKey:
    """
    Dependency to verify the API key from the X-API-Key header.
    Rejects invalid, expired, or revoked keys.
    Enforces rate limiting.
    """
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )

    # 1. Validate key
    api_key = await ApiKeyService.validate_key(db, raw_key)

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API Key",
        )

    if not api_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Revoked API Key",
        )

    # 2. Check Rate Limit
    is_allowed = await RateLimitService.check_rate_limit(api_key.id, api_key.tier)

    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate Limit Exceeded",
        )

    # 3. Attach key to request state for usage tracking
    request.state.api_key = api_key

    # 4. Update last used in background task
    # We will do this in the usage logger to avoid an extra query per request

    return api_key
