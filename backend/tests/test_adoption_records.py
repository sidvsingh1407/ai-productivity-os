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
from models.ai_system import AISystem
from models.adoption_record import AdoptionRecord
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
        email=f"test-{uuid.uuid4().hex[:8]}@example.com",
        full_name="Test User",
        hashed_password="fakehash"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def organization(db_session: AsyncSession):
    org = Organization(name="Test Org", slug=f"test-org-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def user_member(db_session: AsyncSession, user: User, organization: Organization):
    member = OrgMember(user_id=user.id, org_id=organization.id, role=OrgRole.member)
    db_session.add(member)
    await db_session.commit()
    return member

@pytest_asyncio.fixture
async def valid_token(user: User):
    return create_access_token(data={"sub": str(user.id)})

@pytest_asyncio.fixture
async def ai_system(db_session: AsyncSession, organization: Organization):
    system = AISystem(
        organization_id=organization.id,
        name="Test System",
        decision_making_role="not_specified",
        status="active"
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)
    return system

@pytest.mark.asyncio
async def test_create_adoption_record(user_member, valid_token, ai_system):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/adoption-records",
            json={
                "ai_system_id": str(ai_system.id),
                "department": "Engineering",
                "user_count": 10,
                "usage_frequency": "daily",
                "shadow_ai_detected": False,
                "champions": ["Alice", "Bob"],
                "resistance_level": "low",
                "training_status": "in_progress"
            },
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["department"] == "Engineering"
        assert data["user_count"] == 10
        assert data["champions"] == ["Alice", "Bob"]
        assert data["ai_system_id"] == str(ai_system.id)

@pytest.mark.asyncio
async def test_unique_constraint_adoption_record(user_member, valid_token, ai_system):
    payload = {
        "ai_system_id": str(ai_system.id),
        "department": "Engineering",
        "user_count": 10
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create first record
        response1 = await client.post(
            "/api/adoption-records",
            json=payload,
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response1.status_code == 201

        # Attempt to create duplicate record with same system and department
        response2 = await client.post(
            "/api/adoption-records",
            json=payload,
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        # We expect a 409 Conflict error
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"]

@pytest.mark.asyncio
async def test_list_adoption_records(user_member, valid_token, ai_system, db_session, organization):
    # Create two records directly
    r1 = AdoptionRecord(
        organization_id=organization.id,
        ai_system_id=ai_system.id,
        department="HR",
        user_count=5
    )
    r2 = AdoptionRecord(
        organization_id=organization.id,
        ai_system_id=ai_system.id,
        department="Sales",
        user_count=20
    )
    db_session.add_all([r1, r2])
    await db_session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/adoption-records",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Test filtering
        response_filtered = await client.get(
            "/api/adoption-records?department=HR",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response_filtered.status_code == 200
        data_filtered = response_filtered.json()
        assert len(data_filtered) == 1
        assert data_filtered[0]["department"] == "HR"

@pytest.mark.asyncio
async def test_update_adoption_record(user_member, valid_token, ai_system, db_session, organization):
    record = AdoptionRecord(
        organization_id=organization.id,
        ai_system_id=ai_system.id,
        department="Finance",
        user_count=5
    )
    db_session.add(record)
    await db_session.commit()
    await db_session.refresh(record)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put(
            f"/api/adoption-records/{record.id}",
            json={
                "user_count": 15,
                "shadow_ai_detected": True
            },
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_count"] == 15
        assert data["shadow_ai_detected"] is True
        assert data["department"] == "Finance" # Check it didn't change

@pytest.mark.asyncio
async def test_delete_adoption_record(user_member, valid_token, ai_system, db_session, organization):
    record = AdoptionRecord(
        organization_id=organization.id,
        ai_system_id=ai_system.id,
        department="Marketing"
    )
    db_session.add(record)
    await db_session.commit()
    await db_session.refresh(record)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Delete it
        delete_response = await client.delete(
            f"/api/adoption-records/{record.id}",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert delete_response.status_code == 200

        # Try to get it
        get_response = await client.get(
            f"/api/adoption-records/{record.id}",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_cross_org_isolation(db_session, user, valid_token, ai_system, organization):
    # Create another org and user
    other_org = Organization(name="Other Org", slug=f"other-org-{uuid.uuid4().hex[:8]}")
    db_session.add(other_org)

    other_user = User(
        email=f"other-{uuid.uuid4().hex[:8]}@example.com",
        full_name="Other User",
        hashed_password="fakehash"
    )
    db_session.add(other_user)
    await db_session.commit()

    # User is in other_org
    other_member = OrgMember(user_id=other_user.id, org_id=other_org.id, role=OrgRole.member)
    db_session.add(other_member)

    # Put a record in other_org
    other_record = AdoptionRecord(
        organization_id=other_org.id,
        ai_system_id=ai_system.id,  # Sharing system just for test
        department="Marketing"
    )
    db_session.add(other_record)
    await db_session.commit()
    await db_session.refresh(other_record)

    # Original user is in original org, valid_token is for original user
    original_member = OrgMember(user_id=user.id, org_id=organization.id, role=OrgRole.member)
    db_session.add(original_member)
    await db_session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Original user should not be able to get other org's record
        get_response = await client.get(
            f"/api/adoption-records/{other_record.id}",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert get_response.status_code == 404

        # Original user should not see other org's record in list
        list_response = await client.get(
            "/api/adoption-records",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert list_response.status_code == 200
        assert len(list_response.json()) == 0
