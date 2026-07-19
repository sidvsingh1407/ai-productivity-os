import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

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

# Fixtures for user and org
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
async def system_payload():
    return {
        "name": "Test System",
        "purpose": "A test system",
        "data_types": ["personal", "financial"],
        "decision_making_role": "automated",
        "status": "active"
    }

def get_auth_headers(user):
    from dependencies import oauth2_scheme
    from jose import jwt
    from config import settings

    # generate a valid JWT token
    to_encode = {"sub": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"Authorization": f"Bearer {encoded_jwt}"}

@pytest.mark.asyncio
async def test_create_ai_system(db_session: AsyncSession, user, system_payload):
    headers = get_auth_headers(user)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/ai-systems", json=system_payload, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == system_payload["name"]
        assert data["purpose"] == system_payload["purpose"]
        assert data["data_types"] == system_payload["data_types"]
        assert data["decision_making_role"] == system_payload["decision_making_role"]
        assert data["status"] == system_payload["status"]
        assert "id" in data
        assert "organization_id" in data

@pytest.mark.asyncio
async def test_list_ai_systems(db_session: AsyncSession, user, organization: Organization, system_payload):
    headers = get_auth_headers(user)

    # Create system first
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/api/ai-systems", json=system_payload, headers=headers)

        response = await client.get("/api/ai-systems", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["name"] == system_payload["name"]

@pytest.mark.asyncio
async def test_get_ai_system(db_session: AsyncSession, user, organization: Organization, system_payload):
    headers = get_auth_headers(user)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/ai-systems", json=system_payload, headers=headers)
        system_id = create_res.json()["id"]

        get_res = await client.get(f"/api/ai-systems/{system_id}", headers=headers)
        assert get_res.status_code == 200
        assert get_res.json()["id"] == system_id

@pytest.mark.asyncio
async def test_update_ai_system(db_session: AsyncSession, user, organization: Organization, system_payload):
    headers = get_auth_headers(user)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/ai-systems", json=system_payload, headers=headers)
        system_id = create_res.json()["id"]

        update_payload = {"name": "Updated System"}
        update_res = await client.put(f"/api/ai-systems/{system_id}", json=update_payload, headers=headers)
        assert update_res.status_code == 200
        assert update_res.json()["name"] == "Updated System"
        assert update_res.json()["status"] == "active"

@pytest.mark.asyncio
async def test_delete_ai_system(db_session: AsyncSession, user, organization: Organization, system_payload):
    headers = get_auth_headers(user)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/ai-systems", json=system_payload, headers=headers)
        system_id = create_res.json()["id"]

        delete_res = await client.delete(f"/api/ai-systems/{system_id}", headers=headers)
        assert delete_res.status_code == 200

        get_res = await client.get(f"/api/ai-systems/{system_id}", headers=headers)
        assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_ai_system_technology_fields(db_session: AsyncSession, organization: Organization):
    """
    Test that the new technology fields map correctly in SQLAlchemy,
    defaults are applied properly, and types behave as expected.
    """
    sys = AISystem(
        organization_id=organization.id,
        name="Tech Test System",
        vendor="OpenAI",
        model_name="GPT-4",
        model_version="0613",
        api_provider="Azure",
        framework="LangChain",
        hosting="Cloud",
        authentication_method="OAuth2",
        vector_db="Pinecone",
        workflow_engine="Airflow",
        agent_framework="AutoGPT"
    )
    db_session.add(sys)
    await db_session.commit()
    await db_session.refresh(sys)

    assert sys.vendor == "OpenAI"
    assert sys.model_name == "GPT-4"
    assert sys.model_version == "0613"
    assert sys.api_provider == "Azure"
    assert sys.framework == "LangChain"
    assert sys.hosting == "Cloud"
    assert sys.authentication_method == "OAuth2"
    assert sys.vector_db == "Pinecone"
    assert sys.workflow_engine == "Airflow"
    assert sys.agent_framework == "AutoGPT"

    # Test JSONB default properties
    assert sys.integrations == []
    assert sys.knowledge_sources == []

    # Update JSONB fields and test persistence
    sys.integrations = ["Jira", "Slack"]
    sys.knowledge_sources = ["Confluence", "Google Drive"]
    await db_session.commit()
    await db_session.refresh(sys)

    assert sys.integrations == ["Jira", "Slack"]
    assert sys.knowledge_sources == ["Confluence", "Google Drive"]


@pytest.mark.asyncio
async def test_ai_system_ownership_isolation(db_session: AsyncSession, user, user2, system_payload):
    headers1 = get_auth_headers(user)
    headers2 = get_auth_headers(user2)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # User 1 creates system
        create_res = await client.post("/api/ai-systems", json=system_payload, headers=headers1)
        system_id = create_res.json()["id"]

        # User 2 tries to access it
        get_res = await client.get(f"/api/ai-systems/{system_id}", headers=headers2)
        assert get_res.status_code == 404

        # User 2 tries to update it
        update_res = await client.put(f"/api/ai-systems/{system_id}", json={"name": "hacked"}, headers=headers2)
        assert update_res.status_code == 404

        # User 2 tries to delete it
        delete_res = await client.delete(f"/api/ai-systems/{system_id}", headers=headers2)
        assert delete_res.status_code == 404
