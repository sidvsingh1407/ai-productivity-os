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
