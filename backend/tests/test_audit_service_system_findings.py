import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from main import app
from database import engine, Base, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.ai_system import AISystem
from models.audit import Audit, AuditStatus
from models.system_finding import SystemFinding
from models.user import User

from audits.service import run_audit

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
    u = User(email="test@example.com", full_name="Test User", hashed_password="fake")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)

    member = OrgMember(org_id=organization.id, user_id=u.id, role=OrgRole.admin)
    db_session.add(member)
    await db_session.commit()
    return u


@pytest.mark.asyncio
async def test_run_audit_zero_systems(db_session: AsyncSession, organization: Organization, user: User):
    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    result = await run_audit(db_session, organization.id, user.id, form_response)

    # Verify no system findings were created
    stmt = select(SystemFinding)
    res = await db_session.execute(stmt)
    findings = list(res.scalars().all())

    assert len(findings) == 0

@pytest.mark.asyncio
async def test_run_audit_with_systems(db_session: AsyncSession, organization: Organization, user: User):
    # 1. Create some AI systems
    sys1 = AISystem(
        organization_id=organization.id,
        name="Sys 1",
        data_types=["personal"],
        decision_making_role="automated",
        status="active",
        criticality="high"
    )
    sys2 = AISystem(
        organization_id=organization.id,
        name="Sys 2",
        data_types=["public"],
        decision_making_role="advisor",
        status="active",
        criticality="low"
    )

    db_session.add(sys1)
    db_session.add(sys2)
    await db_session.commit()

    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    result = await run_audit(db_session, organization.id, user.id, form_response)

    # Verify system findings were created, exactly one per system
    stmt = select(SystemFinding).where(SystemFinding.audit_id == result.id)
    res = await db_session.execute(stmt)
    findings = list(res.scalars().all())

    assert len(findings) == 2

    sys_ids = [f.ai_system_id for f in findings]
    assert sys1.id in sys_ids
    assert sys2.id in sys_ids

    sys1_finding = next(f for f in findings if f.ai_system_id == sys1.id)
    sys2_finding = next(f for f in findings if f.ai_system_id == sys2.id)

    def get_gov_severity(sf: SystemFinding) -> str:
        # Assuming the finding title is "AI Governance Framework Vulnerability"
        for finding in sf.findings:
            if finding.get("title") == "AI Governance Framework Vulnerability":
                return finding.get("severity")
        return None

    sys1_gov_severity = get_gov_severity(sys1_finding)
    sys2_gov_severity = get_gov_severity(sys2_finding)

    assert sys1_gov_severity is not None
    assert sys2_gov_severity is not None

    # sys1 has high criticality & automated decision making -> bumps governance by 1
    # sys2 has low criticality & advisor -> no bumps for governance
    # Wait, the current form_response might make it Critical (0 score).
    # Let's adjust the test to ensure sys1 has a higher severity than sys2, or modify the test context slightly if needed.
    # We will just verify they are at expected levels. We know the default form response "a" for everything actually gives some points.

    # Severity order: Advisory -> Moderate -> Major -> Critical
    severity_order = {"Advisory": 1, "Moderate": 2, "Major": 3, "Critical": 4}

    assert severity_order[sys1_gov_severity] > severity_order[sys2_gov_severity], \
        f"Expected sys1 ({sys1_gov_severity}) to have higher severity than sys2 ({sys2_gov_severity})"

from auth.jwt_utils import create_access_token

@pytest_asyncio.fixture
async def auth_client(user: User):
    token = create_access_token(data={"sub": str(user.id)})
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers.update({"Authorization": f"Bearer {token}"})
        yield ac

@pytest.mark.asyncio
async def test_api_audit_with_system_findings(auth_client: AsyncClient, db_session: AsyncSession, organization: Organization, user: User):
    # 1. Create an AI system
    sys1 = AISystem(
        organization_id=organization.id,
        name="Test System Endpoint",
        data_types=["personal"],
        decision_making_role="automated",
        status="active",
        criticality="high"
    )
    db_session.add(sys1)
    await db_session.commit()

    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    # 2. POST /api/v1/audits/
    post_resp = await auth_client.post("/audits/", json={"form_response": form_response})
    assert post_resp.status_code == 200
    post_data = post_resp.json()

    assert "system_findings" in post_data
    assert isinstance(post_data["system_findings"], list)
    assert len(post_data["system_findings"]) == 1
    assert post_data["system_findings"][0]["ai_system_name"] == "Test System Endpoint"

    # Ensure linked_finding is stripped
    for sf in post_data["system_findings"]:
        for rec in sf.get("recommendations", []):
            assert "linked_finding" not in rec

    audit_id = post_data["id"]

    # 3. GET /api/v1/audits/{id}
    get_resp = await auth_client.get(f"/audits/{audit_id}")
    assert get_resp.status_code == 200
    get_data = get_resp.json()

    assert "system_findings" in get_data
    assert isinstance(get_data["system_findings"], list)
    assert len(get_data["system_findings"]) == 1
    assert get_data["system_findings"][0]["ai_system_name"] == "Test System Endpoint"

    # Ensure intelligence.findings is properly aggregated and there's findings
    assert "intelligence" in get_data
    assert "findings" in get_data["intelligence"]
    assert len(get_data["intelligence"]["findings"]) > 0

    # Ensure linked_finding is stripped from top-level intelligence recommendations
    for rec in get_data["intelligence"]["recommendations"]:
        assert "linked_finding" not in rec


@pytest.mark.asyncio
async def test_aggregate_top_findings_behavior(auth_client: AsyncClient, db_session: AsyncSession, organization: Organization, user: User):
    # Create multiple AI systems to test deduplication and system counting
    sys1 = AISystem(
        organization_id=organization.id,
        name="Sys 1 (Critical)",
        data_types=["personal"],
        decision_making_role="automated",
        status="active",
        criticality="high"
    )
    sys2 = AISystem(
        organization_id=organization.id,
        name="Sys 2 (Advisory)",
        data_types=["public"],
        decision_making_role="advisor",
        status="active",
        criticality="low"
    )
    db_session.add(sys1)
    db_session.add(sys2)
    await db_session.commit()

    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    # POST /api/v1/audits/
    post_resp = await auth_client.post("/audits/", json={"form_response": form_response})
    assert post_resp.status_code == 200
    data = post_resp.json()

    # Get aggregated intelligence findings
    agg_findings = data["intelligence"]["findings"]
    agg_recs = data["intelligence"]["recommendations"]

    assert len(agg_findings) > 0
    assert len(agg_findings) <= 5  # TOP_FINDINGS_COUNT

    # Re-verify that recommendations were actually populated correctly
    assert len(agg_recs) > 0

    # Ensure system_count is stripped from output schema
    for f in agg_findings:
        assert "system_count" not in f

    # Linked findings should be stripped
    for rec in agg_recs:
        assert "linked_finding" not in rec


@pytest.mark.asyncio
async def test_api_audit_no_system_findings(auth_client: AsyncClient, db_session: AsyncSession, organization: Organization, user: User):
    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    # POST /api/v1/audits/
    post_resp = await auth_client.post("/audits/", json={"form_response": form_response})
    assert post_resp.status_code == 200
    post_data = post_resp.json()

    assert "system_findings" in post_data
    assert isinstance(post_data["system_findings"], list)
    assert len(post_data["system_findings"]) == 0  # Should be empty list

    audit_id = post_data["id"]

    # GET /api/v1/audits/{id}
    get_resp = await auth_client.get(f"/audits/{audit_id}")
    assert get_resp.status_code == 200
    get_data = get_resp.json()

    assert "system_findings" in get_data
    assert isinstance(get_data["system_findings"], list)
    assert len(get_data["system_findings"]) == 0
