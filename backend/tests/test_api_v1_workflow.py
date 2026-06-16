import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import uuid
import asyncio

from main import app
from database import Base, engine, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.user import User
from models.api_platform import ApiKey, ApiTier
from api_platform.service import ApiKeyService

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def setup_api_data():
    async with async_session_maker() as session:
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            email="api_test@tarkax.com",
            hashed_password="hashed_password_test",
            full_name="API Test User",
            is_active=True
        )
        session.add(user)

        org_id = uuid.uuid4()
        org = Organization(id=org_id, name="API Test Org")
        session.add(org)

        member = OrgMember(org_id=org_id, user_id=user_id, role=OrgRole.owner)
        session.add(member)

        api_key, raw_key = await ApiKeyService.create_api_key(
            db=session,
            organization_id=org_id,
            name="Test Key Workflow",
            tier=ApiTier.free,
            is_test=True
        )

        await session.commit()
        return raw_key, org_id

@pytest.mark.asyncio
async def test_workflow_api(setup_api_data):
    raw_key, org_id = setup_api_data

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/workflow",
            json={
                "workflow_name": "Invoice Processing",
                "description": "Current invoice approval process",
                "steps": [
                    {
                        "role": "Finance",
                        "action": "Review invoice"
                    }
                ]
            },
            headers={"X-API-Key": raw_key}
        )

    assert response.status_code == 200
    data = response.json()
    assert "executive_summary" in data
    assert "bottlenecks" in data
    assert data["executive_summary"]["most_critical_bottleneck"] == "Unoptimized Workflow Routines"
