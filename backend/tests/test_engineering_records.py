import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from main import app
from database import engine, Base, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.user import User
from models.engineering_record import EngineeringRecord
from auth.jwt_utils import create_access_token

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
        # Enforce foreign keys in sqlite
        await session.execute(text('PRAGMA foreign_keys=ON;'))
        yield session

@pytest_asyncio.fixture
async def user(db_session: AsyncSession):
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashed_password",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def organization(db_session: AsyncSession):
    org = Organization(name="Test Org", slug="test-org")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def user_member(db_session: AsyncSession, user: User, organization: Organization):
    member = OrgMember(
        user_id=user.id,
        org_id=organization.id,
        role=OrgRole.admin
    )
    db_session.add(member)
    await db_session.commit()
    return member

@pytest.fixture
def valid_token(user: User, organization: Organization):
    return create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "org_id": str(organization.id)
        }
    )

@pytest.mark.asyncio
async def test_create_engineering_record(user_member, valid_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "has_dedicated_ai_team": True,
            "team_size": 5,
            "roles": ["Data Scientist", "ML Engineer"],
            "has_mlops_pipeline": True,
            "monitoring_tooling": ["Prometheus", "Grafana"],
            "has_dedicated_devops": True,
            "ai_engineering_budget": 500000.0,
            "has_dedicated_prompt_engineer": True
        }

        response = await client.post(
            "/api/engineering-records",
            json=payload,
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["has_dedicated_ai_team"] is True
        assert data["team_size"] == 5
        assert len(data["roles"]) == 2
        # Score calculation check:
        # team = 25, mlops = 25, tooling = 15, devops = 15, prompt = 10, budget = 10
        # total = 25+25+15+15+10+10 = 100
        assert data["engineering_score"] == 100.0

@pytest.mark.asyncio
async def test_unique_constraint_engineering_record(user_member, valid_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "has_dedicated_ai_team": False,
            "team_size": 1
        }

        res1 = await client.post(
            "/api/engineering-records",
            json=payload,
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert res1.status_code == 201

        res2 = await client.post(
            "/api/engineering-records",
            json=payload,
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert res2.status_code == 409

@pytest.mark.asyncio
async def test_list_engineering_records(user_member, valid_token, db_session, organization):
    r1 = EngineeringRecord(
        organization_id=organization.id,
        has_dedicated_ai_team=False,
        team_size=0,
        has_mlops_pipeline=False
    )
    db_session.add(r1)
    await db_session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/engineering-records",
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["engineering_score"] == 0.0

@pytest.mark.asyncio
async def test_update_engineering_record(user_member, valid_token, db_session, organization):
    record = EngineeringRecord(
        organization_id=organization.id,
        has_dedicated_ai_team=False,
        team_size=0,
    )
    db_session.add(record)
    await db_session.commit()
    await db_session.refresh(record)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "has_dedicated_ai_team": True,
            "team_size": 10
        }

        response = await client.put(
            f"/api/engineering-records/{record.id}",
            json=payload,
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["has_dedicated_ai_team"] is True
        assert data["team_size"] == 10
        assert data["engineering_score"] == 25.0

@pytest.mark.asyncio
async def test_delete_engineering_record(user_member, valid_token, db_session, organization):
    record = EngineeringRecord(
        organization_id=organization.id,
        has_dedicated_ai_team=True,
    )
    db_session.add(record)
    await db_session.commit()
    await db_session.refresh(record)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(
            f"/api/engineering-records/{record.id}",
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        assert response.status_code == 200

        # Verify it's gone
        res2 = await client.get(
            f"/api/engineering-records/{record.id}",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert res2.status_code == 404
