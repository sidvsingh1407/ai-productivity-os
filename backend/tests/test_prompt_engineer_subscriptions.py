import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from main import app
from database import engine, Base, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.prompt_engineer_subscription import PromptEngineerSubscription

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
    test_user = User(
        email=f"user1_{uuid.uuid4().hex[:8]}@example.com",
        hashed_password="fakehash",
        full_name="Test User"
    )
    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)

    member = OrgMember(
        user_id=test_user.id,
        org_id=organization.id,
        role=OrgRole.owner
    )
    db_session.add(member)
    await db_session.commit()

    return test_user

@pytest_asyncio.fixture
async def user2(db_session: AsyncSession):
    from models.user import User
    # Second user in a different organization
    org2 = Organization(name="Test Org 2", slug=f"test-org-2-{uuid.uuid4().hex[:8]}")
    db_session.add(org2)
    await db_session.commit()
    await db_session.refresh(org2)

    test_user2 = User(
        email=f"user2_{uuid.uuid4().hex[:8]}@example.com",
        hashed_password="fakehash",
        full_name="Test User 2"
    )
    db_session.add(test_user2)
    await db_session.commit()
    await db_session.refresh(test_user2)

    member2 = OrgMember(
        user_id=test_user2.id,
        org_id=org2.id,
        role=OrgRole.owner
    )
    db_session.add(member2)
    await db_session.commit()

    return test_user2

def get_auth_headers(user):
    from auth.jwt_utils import create_access_token
    token = create_access_token(data={"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def subscription_payload():
    return {
        "plan_tier": "unset",
        "status": "active",
        "external_subscription_id": "sub_12345",
        "seat_count": 5,
        "billing_cycle": "monthly"
    }

@pytest.mark.asyncio
async def test_create_prompt_engineer_subscription(db_session: AsyncSession, user, subscription_payload):
    headers = get_auth_headers(user)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/prompt-engineer-subscriptions", json=subscription_payload, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert data["plan_tier"] == subscription_payload["plan_tier"]
        assert data["status"] == subscription_payload["status"]
        assert data["external_subscription_id"] == subscription_payload["external_subscription_id"]
        assert data["seat_count"] == subscription_payload["seat_count"]
        assert data["billing_cycle"] == subscription_payload["billing_cycle"]

@pytest.mark.asyncio
async def test_list_prompt_engineer_subscriptions(db_session: AsyncSession, user, subscription_payload):
    headers = get_auth_headers(user)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create one
        await client.post("/api/prompt-engineer-subscriptions", json=subscription_payload, headers=headers)

        response = await client.get("/api/prompt-engineer-subscriptions", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["plan_tier"] == subscription_payload["plan_tier"]

@pytest.mark.asyncio
async def test_get_prompt_engineer_subscription(db_session: AsyncSession, user, subscription_payload):
    headers = get_auth_headers(user)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/prompt-engineer-subscriptions", json=subscription_payload, headers=headers)
        sub_id = create_res.json()["id"]

        get_res = await client.get(f"/api/prompt-engineer-subscriptions/{sub_id}", headers=headers)
        assert get_res.status_code == status.HTTP_200_OK
        data = get_res.json()
        assert data["id"] == sub_id
        assert data["plan_tier"] == subscription_payload["plan_tier"]

@pytest.mark.asyncio
async def test_update_prompt_engineer_subscription(db_session: AsyncSession, user, subscription_payload):
    headers = get_auth_headers(user)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/prompt-engineer-subscriptions", json=subscription_payload, headers=headers)
        sub_id = create_res.json()["id"]

        update_payload = {"plan_tier": "upgraded", "seat_count": 10}
        update_res = await client.put(f"/api/prompt-engineer-subscriptions/{sub_id}", json=update_payload, headers=headers)
        assert update_res.status_code == status.HTTP_200_OK
        data = update_res.json()
        assert data["plan_tier"] == "upgraded"
        assert data["seat_count"] == 10
        # Should keep original fields for the rest
        assert data["status"] == subscription_payload["status"]

@pytest.mark.asyncio
async def test_delete_prompt_engineer_subscription(db_session: AsyncSession, user, subscription_payload):
    headers = get_auth_headers(user)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/prompt-engineer-subscriptions", json=subscription_payload, headers=headers)
        sub_id = create_res.json()["id"]

        delete_res = await client.delete(f"/api/prompt-engineer-subscriptions/{sub_id}", headers=headers)
        assert delete_res.status_code == status.HTTP_200_OK

        get_res = await client.get(f"/api/prompt-engineer-subscriptions/{sub_id}", headers=headers)
        assert get_res.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_prompt_engineer_subscription_ownership_isolation(db_session: AsyncSession, user, user2, subscription_payload):
    headers1 = get_auth_headers(user)
    headers2 = get_auth_headers(user2)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # User 1 creates subscription
        create_res = await client.post("/api/prompt-engineer-subscriptions", json=subscription_payload, headers=headers1)
        sub_id = create_res.json()["id"]

        # User 2 tries to access it
        get_res = await client.get(f"/api/prompt-engineer-subscriptions/{sub_id}", headers=headers2)
        assert get_res.status_code == status.HTTP_404_NOT_FOUND

        # User 2 tries to update it
        update_res = await client.put(f"/api/prompt-engineer-subscriptions/{sub_id}", json={"plan_tier": "hacked"}, headers=headers2)
        assert update_res.status_code == status.HTTP_404_NOT_FOUND

        # User 2 tries to delete it
        delete_res = await client.delete(f"/api/prompt-engineer-subscriptions/{sub_id}", headers=headers2)
        assert delete_res.status_code == status.HTTP_404_NOT_FOUND
