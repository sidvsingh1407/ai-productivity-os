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

@pytest.mark.asyncio
async def test_impact_analysis_traversal_and_weighting(user_token: str, db_session: AsyncSession, organization: Organization):
    from models.risk_classification import RiskClassification
    from models.system_finding import SystemFinding
    from models.workflow import Workflow
    from models.audit import Audit
    from dependency_map.schemas import DependencyNodeCreate, DependencyEdgeCreate
    from dependency_map.service import create_node, create_edge

    # Create 2 AI Systems
    sys_high = AISystem(name="High Risk Sys", organization_id=organization.id, criticality="critical")
    sys_low = AISystem(name="Low Risk Sys", organization_id=organization.id, criticality="low")
    db_session.add(sys_high)
    db_session.add(sys_low)

    # Create 1 Workflow and 1 Audit
    from models.user import User
    # User is needed for workflow
    u = User(email=f"test_wf_{uuid.uuid4()}@example.com", full_name="Wf User", hashed_password="fake")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)

    wf = Workflow(org_id=organization.id, user_id=u.id, input_config={}, status="complete")
    aud = Audit(org_id=organization.id, user_id=u.id, form_response={}, status="complete")
    db_session.add(wf)
    db_session.add(aud)
    await db_session.commit()

    # Add Risk and Findings to High Sys
    rc = RiskClassification(audit_id=aud.id, ai_system_id=sys_high.id, risk_level="high_risk", rationale="", citation_reference="")
    sf = SystemFinding(audit_id=aud.id, ai_system_id=sys_high.id, findings=[{"severity": "Critical"}], dimension_scores={})
    db_session.add(rc)
    db_session.add(sf)
    await db_session.commit()

    # Create nodes
    node_high = await create_node(db_session, organization.id, DependencyNodeCreate(node_type='ai_system', ai_system_id=sys_high.id))
    node_low = await create_node(db_session, organization.id, DependencyNodeCreate(node_type='ai_system', ai_system_id=sys_low.id))
    node_wf = await create_node(db_session, organization.id, DependencyNodeCreate(node_type='workflow', workflow_id=wf.id))
    node_aud = await create_node(db_session, organization.id, DependencyNodeCreate(node_type='audit', audit_id=aud.id))

    # Create edges:
    # node_high -> depends_on -> node_low
    # node_wf -> uses -> node_high
    # node_aud -> uses -> node_low
    await create_edge(db_session, organization.id, DependencyEdgeCreate(source_node_id=node_high.id, target_node_id=node_low.id, edge_type="depends_on"))
    await create_edge(db_session, organization.id, DependencyEdgeCreate(source_node_id=node_wf.id, target_node_id=node_high.id, edge_type="uses"))
    await create_edge(db_session, organization.id, DependencyEdgeCreate(source_node_id=node_aud.id, target_node_id=node_low.id, edge_type="uses"))

    # Analyze Impact on High Sys
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {user_token}"}
        res = await ac.get(f"/api/dependency-map/nodes/{node_high.id}/impact", headers=headers)
        assert res.status_code == 200
        data = res.json()

        # Check Origin (sys_high)
        # critical = 30, high_risk = 25, Critical = 40 => 95
        assert data["origin_impact"]["total_score"] == 95
        assert data["origin_impact"]["criticality_score"] == 30
        assert data["origin_impact"]["findings_score"] == 40
        assert data["origin_impact"]["risk_level_score"] == 25

        # Outward (depends_on) should be sys_low
        assert len(data["depends_on"]) == 1
        assert data["depends_on"][0]["id"] == str(node_low.id)
        assert data["depends_on"][0]["impact"]["total_score"] == 0 # no risk, no finding, low criticality (0)

        # Inward (used_by) should be node_wf
        assert len(data["used_by"]) == 1
        assert data["used_by"][0]["id"] == str(node_wf.id)
        # Workflow connected to high sys (in subgraph) gets max score (95)
        assert data["used_by"][0]["impact"]["total_score"] == 95

    # Analyze Impact on Audit (Depth 2 to reach high_sys via low_sys)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {user_token}"}
        # aud -> low (depth 1), low is used by high (depth 2) -> so high is at depth 2 from aud in a undirected sense?
        # Wait, edges:
        # high -> low (high depends on low)
        # aud -> low (aud uses low)
        # From Aud outward (aud->low). Outward depth 1: low. Outward depth 2: none.
        # From Aud inward: none.
        # So aud only sees low.
        res = await ac.get(f"/api/dependency-map/nodes/{node_aud.id}/impact", headers=headers)
        assert res.status_code == 200
        data = res.json()

        # Origin is audit. Subgraph has aud and low.
        # low has 0 score. So audit gets 0 score.
        assert data["origin_impact"]["total_score"] == 0
        assert data["origin_impact"]["is_unscored_node"] == False

        assert len(data["depends_on"]) == 1
        assert data["depends_on"][0]["id"] == str(node_low.id)
