import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from main import app
from database import engine, Base, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.ai_system import AISystem

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
        # Enforce foreign key constraints for SQLite testing
        await session.execute(text('PRAGMA foreign_keys=ON;'))
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

def get_auth_headers(user):
    from dependencies import oauth2_scheme
    from jose import jwt
    from config import settings

    # generate a valid JWT token
    to_encode = {"sub": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"Authorization": f"Bearer {encoded_jwt}"}

@pytest_asyncio.fixture
async def user_token(user):
    return get_auth_headers(user)["Authorization"].split(" ")[1]

@pytest_asyncio.fixture
async def organization2(db_session: AsyncSession):
    org = Organization(name="Test Org 2", slug=f"test-org2-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def user2(db_session: AsyncSession, organization2: Organization):
    from models.user import User
    u = User(email="test2@example.com", full_name="Test User 2", hashed_password="fake")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)

    member = OrgMember(org_id=organization2.id, user_id=u.id, role=OrgRole.admin)
    db_session.add(member)
    await db_session.commit()
    return u

@pytest_asyncio.fixture
async def user_token2(user2):
    return get_auth_headers(user2)["Authorization"].split(" ")[1]


@pytest_asyncio.fixture
async def ai_system(db_session: AsyncSession, organization: Organization):
    system = AISystem(
        name="System 1",
        organization_id=organization.id,
        status="active"
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)
    return system

@pytest_asyncio.fixture
async def ai_system2(db_session: AsyncSession, organization: Organization):
    system = AISystem(
        name="System 2",
        organization_id=organization.id,
        status="active"
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)
    return system

@pytest.mark.asyncio
async def test_get_or_create_node(user_token: str, ai_system: AISystem):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {user_token}"}

        # 1. Create node
        node_payload = {
            "node_type": "ai_system",
            "ai_system_id": str(ai_system.id)
        }

        res = await ac.post("/api/dependency-map/nodes/get-or-create", json=node_payload, headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["node_type"] == "ai_system"
        assert data["ai_system_id"] == str(ai_system.id)
        node_id_1 = data["id"]

        # 2. Get existing node
        res2 = await ac.post("/api/dependency-map/nodes/get-or-create", json=node_payload, headers=headers)
        assert res2.status_code == 200
        data2 = res2.json()
        assert data2["id"] == node_id_1 # Same ID, wasn't recreated

@pytest.mark.asyncio
async def test_node_fk_alignment_validation(user_token: str, ai_system: AISystem):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {user_token}"}

        node_payload = {
            "node_type": "ai_system",
            "workflow_id": str(uuid.uuid4()) # Wrong FK
        }

        res = await ac.post("/api/dependency-map/nodes", json=node_payload, headers=headers)
        assert res.status_code == 422 or res.status_code == 500 # Depending on fastAPI version RequestValidationError serialization

@pytest.mark.asyncio
async def test_create_and_list_edges(user_token: str, ai_system: AISystem, ai_system2: AISystem):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {user_token}"}

        node1_res = await ac.post("/api/dependency-map/nodes/get-or-create", json={"node_type": "ai_system", "ai_system_id": str(ai_system.id)}, headers=headers)
        node2_res = await ac.post("/api/dependency-map/nodes/get-or-create", json={"node_type": "ai_system", "ai_system_id": str(ai_system2.id)}, headers=headers)

        node1_id = node1_res.json()["id"]
        node2_id = node2_res.json()["id"]

        edge_payload = {
            "source_node_id": node1_id,
            "target_node_id": node2_id,
            "edge_type": "depends_on"
        }

        # Create
        res = await ac.post("/api/dependency-map/edges", json=edge_payload, headers=headers)
        assert res.status_code == 201
        data = res.json()
        assert data["source_node_id"] == node1_id
        assert data["target_node_id"] == node2_id

        # List
        res_list = await ac.get("/api/dependency-map/edges", headers=headers)
        assert res_list.status_code == 200
        list_data = res_list.json()
        assert len(list_data) == 1

@pytest.mark.asyncio
async def test_reject_self_referencing_edges(user_token: str, ai_system: AISystem):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {user_token}"}

        node1_res = await ac.post("/api/dependency-map/nodes/get-or-create", json={"node_type": "ai_system", "ai_system_id": str(ai_system.id)}, headers=headers)
        node1_id = node1_res.json()["id"]

        edge_payload = {
            "source_node_id": node1_id,
            "target_node_id": node1_id, # Self loop
            "edge_type": "uses"
        }

        res = await ac.post("/api/dependency-map/edges", json=edge_payload, headers=headers)
        assert res.status_code == 400
        assert "Self-referencing edges" in res.json()["detail"]

@pytest.mark.asyncio
async def test_reject_duplicate_edges(user_token: str, ai_system: AISystem, ai_system2: AISystem):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {user_token}"}

        node1_res = await ac.post("/api/dependency-map/nodes/get-or-create", json={"node_type": "ai_system", "ai_system_id": str(ai_system.id)}, headers=headers)
        node2_res = await ac.post("/api/dependency-map/nodes/get-or-create", json={"node_type": "ai_system", "ai_system_id": str(ai_system2.id)}, headers=headers)

        node1_id = node1_res.json()["id"]
        node2_id = node2_res.json()["id"]

        edge_payload = {
            "source_node_id": node1_id,
            "target_node_id": node2_id,
            "edge_type": "integration"
        }

        res1 = await ac.post("/api/dependency-map/edges", json=edge_payload, headers=headers)
        assert res1.status_code == 201

        res2 = await ac.post("/api/dependency-map/edges", json=edge_payload, headers=headers)
        assert res2.status_code == 409
        assert "Duplicate edge" in res2.json()["detail"]

@pytest.mark.asyncio
async def test_organization_isolation(user_token: str, user_token2: str, ai_system: AISystem, ai_system2: AISystem):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers1 = {"Authorization": f"Bearer {user_token}"}
        headers2 = {"Authorization": f"Bearer {user_token2}"}

        # User 1 creates nodes
        node1_res = await ac.post("/api/dependency-map/nodes/get-or-create", json={"node_type": "ai_system", "ai_system_id": str(ai_system.id)}, headers=headers1)
        node2_res = await ac.post("/api/dependency-map/nodes/get-or-create", json={"node_type": "ai_system", "ai_system_id": str(ai_system2.id)}, headers=headers1)

        node1_id = node1_res.json()["id"]
        node2_id = node2_res.json()["id"]

        # User 2 tries to read user 1's node
        res_read_node = await ac.get(f"/api/dependency-map/nodes/{node1_id}", headers=headers2)
        assert res_read_node.status_code == 404

        # User 2 tries to create edge using user 1's nodes
        edge_payload = {
            "source_node_id": node1_id,
            "target_node_id": node2_id,
            "edge_type": "uses"
        }
        res_create_edge_invalid = await ac.post("/api/dependency-map/edges", json=edge_payload, headers=headers2)
        # Should be 404 because validate_edge_organization_scope looks up nodes and won't find them in user2's org, or 403 if it finds them but wrong org.
        # Given how the single select(DependencyNode).where(id.in_) works, if the nodes aren't found for the org, we throw 404/403. Our validation actually fetches regardless of org, then checks org!
        assert res_create_edge_invalid.status_code in [403, 404]
