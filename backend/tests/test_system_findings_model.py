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
async def test_system_finding_creation_and_fields(db_session: AsyncSession, organization: Organization, user: User):
    """
    Test that the SystemFinding model can be created, properly uses foreign keys,
    and handles JSONB default structures correctly.
    """

    # 1. Create a real Audit
    audit = Audit(
        org_id=organization.id,
        user_id=user.id,
        form_response={"foo": "bar"},
        status=AuditStatus.pending
    )
    db_session.add(audit)

    # 2. Create a real AISystem
    ai_system = AISystem(
        organization_id=organization.id,
        name="Test AI System",
        data_types=["text"],
        decision_making_role="advisor",
        status="active"
    )
    db_session.add(ai_system)

    await db_session.commit()
    await db_session.refresh(audit)
    await db_session.refresh(ai_system)

    # 3. Create the SystemFinding
    finding = SystemFinding(
        audit_id=audit.id,
        ai_system_id=ai_system.id,
        executive_summary="This system is generally compliant."
    )
    db_session.add(finding)
    await db_session.commit()
    await db_session.refresh(finding)

    # Verify the finding was saved properly
    assert finding.id is not None
    assert finding.audit_id == audit.id
    assert finding.ai_system_id == ai_system.id
    assert finding.executive_summary == "This system is generally compliant."

    # Check default JSON structures
    assert finding.findings == []
    assert finding.recommendations == []
    assert finding.dimension_scores == {}

    # Verify auto-generated timestamps exist
    assert finding.created_at is not None
    assert finding.updated_at is not None

    # 4. Update the JSON fields and test persistence
    finding.findings = [{"id": "F-01", "description": "Minor gap found"}]
    finding.recommendations = [{"id": "R-01", "action": "Update docs"}]
    finding.dimension_scores = {"security": 85, "transparency": 90}

    await db_session.commit()
    await db_session.refresh(finding)

    # 5. Retrieve explicitly to confirm DB-level storage
    stmt = select(SystemFinding).where(SystemFinding.id == finding.id)
    result = await db_session.execute(stmt)
    retrieved_finding = result.scalar_one()

    assert len(retrieved_finding.findings) == 1
    assert retrieved_finding.findings[0]["id"] == "F-01"
    assert len(retrieved_finding.recommendations) == 1
    assert retrieved_finding.dimension_scores["security"] == 85

    # Verify relationships are loaded correctly (basic sanity check)
    assert retrieved_finding.audit_id == audit.id
    assert retrieved_finding.ai_system_id == ai_system.id
