import pytest
import pytest_asyncio
import uuid
import time
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends

from database import Base, engine, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.api_platform import ApiTier, ApiKey
from models.audit import Audit, AuditStatus
from api_platform import ApiKeyService, verify_api_key, APIKeyRoute

from main import app

@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_db():
    async with engine.begin() as conn:
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
async def user(db_session: AsyncSession, organization: Organization):
    from models.user import User
    u = User(email="test@example.com", full_name="Test User", hashed_password="fake")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)

    member = OrgMember(org_id=organization.id, user_id=u.id, role=OrgRole.admin)
    db_session.add(member)
    await db_session.commit()
    return u

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

@pytest.mark.asyncio
async def test_audit_api(db_session: AsyncSession, user, organization: Organization, api_key_fixture):
    api_key, raw_key = api_key_fixture

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        form_response = {
            "q2_1": "a", "q2_2": "a", "q2_3": "a",
            "q3_1": "a", "q3_2": "a", "q3_3": "a",
            "q4_1": "a", "q4_2": "a", "q4_3": "a",
            "q5_1": "a", "q5_2": "a", "q5_3": "a"
        }

        response = await client.post(
            "/api/v1/audit",
            headers={"X-API-Key": raw_key},
            json={"form_response": form_response}
        )

        assert response.status_code == 200
        data = response.json()
        assert "overall_score" not in data # Wait, my model has total_score, let's just check standard fields
        assert data["status"] == "complete"
        assert "intelligence" in data
        assert data["total_score"] > 0

@pytest.mark.asyncio
async def test_risk_api(db_session: AsyncSession, user, organization: Organization, api_key_fixture):
    api_key, raw_key = api_key_fixture

    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    # 1. create audit
    from audits.repository import create_audit, save_audit_scores
    from audits.scoring_engine import score_response
    audit = await create_audit(db_session, organization.id, user.id, form_response)
    scores = score_response(form_response, None)
    await save_audit_scores(db_session, audit.id, scores)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/risk",
            headers={"X-API-Key": raw_key},
            json={"audit_id": str(audit.id)}
        )

        assert response.status_code == 200
        data = response.json()
        assert "risk_level" in data
        assert "risk_score" in data
        assert "risk_trend" in data
        assert "risk_drivers" in data
