import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from main import app
from database import Base, engine, async_session_maker
from models.user import User
from models.organization import Organization, OrgMember, OrgRole
from auth.password_service import PasswordService
from sqlalchemy.future import select

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with async_session_maker() as session:
        yield session

async def setup_test_user(db_session, email="test_del@example.com", is_owner=False):
    # Ensure system user exists
    system_user_id = uuid.UUID('00000000-0000-0000-0000-000000000000')
    stmt = select(User).where(User.id == system_user_id)
    result = await db_session.execute(stmt)
    sys_user = result.scalar_one_or_none()
    if not sys_user:
        sys_user = User(
            id=system_user_id,
            email="deleted@system.tarkax.local",
            hashed_password="",
            full_name="Deleted User",
            is_active=False
        )
        db_session.add(sys_user)
        await db_session.commit()

    user = User(
        email=email,
        hashed_password=PasswordService().hash_password("password123"),
        full_name="Test User",
        is_active=True, email_verified=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    org = Organization(name=f"{email}_org", slug=f"org_{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)

    role = OrgRole.owner if is_owner else OrgRole.viewer
    member = OrgMember(user_id=user.id, org_id=org.id, role=role)
    db_session.add(member)

    if not is_owner:
        # Add another admin so they are not the sole admin
        other_user = User(
            email=f"other_{email}",
            hashed_password=PasswordService().hash_password("password123"),
            full_name="Other User",
            is_active=True, email_verified=True
        )
        db_session.add(other_user)
        await db_session.commit()
        await db_session.refresh(other_user)

        other_member = OrgMember(user_id=other_user.id, org_id=org.id, role=OrgRole.admin)
        db_session.add(other_member)

    await db_session.commit()

    return user, org

async def get_test_token(client: AsyncClient, email: str):
    response = await client.post(
        "/auth/login",
        json={"email": email, "password": "password123"}
    )
    return response.json()["access_token"]

async def test_standard_user_deletion(db_session):
    user, org = await setup_test_user(db_session, "standard@example.com", is_owner=False)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await get_test_token(client, "standard@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.delete("/api/account/delete", headers=headers)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # Verify db changes
        stmt = select(User).where(User.id == user.id)
        result = await db_session.execute(stmt)
        deleted_user = result.scalar_one()

        # Need to refresh the db_session to get updated values
        await db_session.refresh(user)

        assert user.is_active == False
        assert user.hashed_password == ""
        assert user.full_name == "Deleted User"
        assert user.email.startswith("deleted_")

        # Verify memberships removed
        stmt = select(OrgMember).where(OrgMember.user_id == user.id)
        result = await db_session.execute(stmt)
        memberships = result.scalars().all()
        assert len(memberships) == 0

async def test_organization_owner_deletion(db_session):
    user, org = await setup_test_user(db_session, "owner@example.com", is_owner=True)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await get_test_token(client, "owner@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.delete("/api/account/delete", headers=headers)
        assert response.status_code == 400
        data = response.json()

        # The exception detail is a dict, but fastAPI wraps it in {"detail": <content>}
        # OR it just returns what was passed. Let's handle both.
        error_data = data.get("detail", data)
        if isinstance(error_data, str):
            import json
            try:
                error_data = json.loads(error_data.replace("'", '"'))
            except Exception:
                pass

        assert error_data["error"]["code"] == "OWNER_TRANSFER_REQUIRED"
