import pytest
import pytest_asyncio
import uuid
import time
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport, ASGITransport

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends

from database import Base, engine, async_session_maker
from models.organization import Organization
from models.api_platform import ApiTier, ApiKey, ApiUsageLog
from api_platform import ApiKeyService, verify_api_key, APIKeyRoute, RateLimitService

# Ensure db schema exists
@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

@pytest_asyncio.fixture
async def organization(db_session: AsyncSession):
    org = Organization(name="Test Org", slug=f"test-org-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def api_key_fixture(db_session: AsyncSession, organization: Organization):
    api_key, raw_key = await ApiKeyService.create_api_key(
        db=db_session,
        organization_id=organization.id,
        name="Test Key",
        tier=ApiTier.free,
        is_test=True
    )
    return api_key, raw_key

# Setting up a test app with the route and dependency
app = FastAPI()

app.router.route_class = APIKeyRoute

@app.get("/test-endpoint")
async def _test_endpoint(api_key: ApiKey = Depends(verify_api_key)):
    return {"message": "Success", "key_name": api_key.name}

@pytest.mark.asyncio
async def test_key_generation_and_hashing():
    raw_key = ApiKeyService.generate_key(is_test=True)
    assert raw_key.startswith("tkx_test_")
    assert len(raw_key) > 40

    hashed_key = ApiKeyService.hash_key(raw_key)
    assert hashed_key != raw_key
    assert len(hashed_key) == 64

@pytest.mark.asyncio
async def test_create_api_key(db_session: AsyncSession, organization: Organization):
    api_key, raw_key = await ApiKeyService.create_api_key(
        db=db_session,
        organization_id=organization.id,
        name="Backend Key",
        tier=ApiTier.free,
        is_test=True
    )
    assert api_key.name == "Backend Key"
    assert api_key.tier == ApiTier.free
    assert api_key.is_active is True
    assert raw_key.startswith("tkx_test_")
    assert api_key.key_hash == ApiKeyService.hash_key(raw_key)

@pytest.mark.asyncio
async def test_valid_key_access_granted(api_key_fixture):
    api_key, raw_key = api_key_fixture

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/test-endpoint",
                headers={"X-API-Key": raw_key}
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Success", "key_name": api_key.name}

@pytest.mark.asyncio
async def test_invalid_key_rejected():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/test-endpoint",
                headers={"X-API-Key": "tkx_test_invalid123"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired API Key"

@pytest.mark.asyncio
async def test_expired_key_rejected(db_session: AsyncSession, organization: Organization):
    past_date = datetime.now(timezone.utc) - timedelta(days=1)

    api_key, raw_key = await ApiKeyService.create_api_key(
        db=db_session,
        organization_id=organization.id,
        name="Expired Key",
        expires_at=past_date
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/test-endpoint",
                headers={"X-API-Key": raw_key}
        )

        assert response.status_code == 401

@pytest.mark.asyncio
async def test_revoked_key_rejected(db_session: AsyncSession, api_key_fixture):
    api_key, raw_key = api_key_fixture

    await ApiKeyService.revoke_key(db_session, api_key.id)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/test-endpoint",
                headers={"X-API-Key": raw_key}
        )

        assert response.status_code == 403
        assert response.json()["detail"] == "Revoked API Key"

@pytest.mark.asyncio
async def test_rate_limit_exceeded(db_session: AsyncSession, organization: Organization, monkeypatch):
    api_key, raw_key = await ApiKeyService.create_api_key(
        db=db_session,
        organization_id=organization.id,
        name="Rate Limited Key",
        tier=ApiTier.free
    )

    # Mock the rate limiter to return False
    async def mock_check_rate_limit(key_id, tier):
        return False

    monkeypatch.setattr(RateLimitService, "check_rate_limit", mock_check_rate_limit)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/test-endpoint",
                headers={"X-API-Key": raw_key}
        )

        assert response.status_code == 429
        assert response.json()["detail"] == "Rate Limit Exceeded"

@pytest.mark.asyncio
async def test_usage_log_created(db_session: AsyncSession, organization: Organization):
    api_key, raw_key = await ApiKeyService.create_api_key(
        db=db_session,
        organization_id=organization.id,
        name="Logging Key"
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/test-endpoint",
                headers={"X-API-Key": raw_key}
        )
        assert response.status_code == 200

    # Wait a tiny bit for the background task
    import asyncio
    await asyncio.sleep(0.1)

    # Check if usage log was created
    from sqlalchemy import select
    result = await db_session.execute(select(ApiUsageLog).where(ApiUsageLog.api_key_id == api_key.id))
    log = result.scalar_one_or_none()

    assert log is not None
    assert log.endpoint == "/test-endpoint"
    assert log.request_method == "GET"
    assert log.response_status == 200
    assert log.latency_ms > 0

    # Check if last_used_at was updated
    await db_session.refresh(api_key)
    assert api_key.last_used_at is not None
