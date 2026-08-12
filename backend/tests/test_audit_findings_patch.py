import pytest
import uuid
from httpx import AsyncClient
from main import app
from dependencies import get_db, require_role, get_current_user, get_current_org
from models.user import User
from models.organization import Organization, OrgMember
from sqlalchemy.ext.asyncio import AsyncSession
from tests.test_ai_systems import setup_db, db_session

@pytest.fixture
def mock_user():
    return User(id=uuid.uuid4(), email="test@test.com", hashed_password="mock", full_name="Mock User", is_active=True)

@pytest.fixture
def mock_org():
    return Organization(id=uuid.uuid4(), name="Test Org")

@pytest.mark.asyncio
async def test_update_system_finding_endpoint(mock_user, mock_org, db_session: AsyncSession):
    # Setup test data
    from models.audit import Audit, AuditStatus
    from models.ai_system import AISystem
    from models.system_finding import SystemFinding

    audit_id = uuid.uuid4()
    org_id = mock_org.id

    db_session.add(mock_user)
    db_session.add(mock_org)
    await db_session.flush()

    member = OrgMember(user_id=mock_user.id, org_id=org_id, role="member")
    db_session.add(member)
    await db_session.flush()

    # Create audit
    audit = Audit(
        id=audit_id,
        org_id=org_id,
        user_id=mock_user.id,
        status=AuditStatus.complete,
        form_response={}
    )
    db_session.add(audit)

    # Create ai system
    sys_id = uuid.uuid4()
    ai_system = AISystem(
        id=sys_id,
        organization_id=org_id,
        name="Test System",
        ai_type="genai"
    )
    db_session.add(ai_system)

    # Create system finding
    sf_id = uuid.uuid4()
    sf = SystemFinding(
        id=sf_id,
        audit_id=audit_id,
        ai_system_id=sys_id,
        findings=[
            {"title": "Finding 1", "severity": "High", "impact": "Bad", "rationale": "Because"},
            {"title": "Finding 2", "severity": "Low", "impact": "Okay", "rationale": "Just so"}
        ],
        recommendations=[],
        dimension_scores={}
    )
    db_session.add(sf)
    await db_session.commit()

    # Override dependencies
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_current_org] = lambda: mock_org
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Valid patch
        resp = await ac.patch(
            f"/audits/{audit_id}/system-findings/{sf_id}/findings/Finding%201",
            json={"lifecycle_stage": "deployment", "ethical_dimension": "accuracy"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["findings"]) == 2

        f1 = next(f for f in data["findings"] if f["title"] == "Finding 1")
        assert f1["lifecycle_stage"] == "deployment"
        assert f1["ethical_dimension"] == "accuracy"

        # Patch just one field
        resp2 = await ac.patch(
            f"/audits/{audit_id}/system-findings/{sf_id}/findings/Finding%202",
            json={"lifecycle_stage": "data_input"}
        )
        assert resp2.status_code == 200
        data2 = resp2.json()
        f2 = next(f for f in data2["findings"] if f["title"] == "Finding 2")
        assert f2["lifecycle_stage"] == "data_input"
        assert f2.get("ethical_dimension") is None

        # Invalid patch (no fields)
        resp3 = await ac.patch(
            f"/audits/{audit_id}/system-findings/{sf_id}/findings/Finding%201",
            json={}
        )
        assert resp3.status_code == 422

        # Non-existent finding
        resp4 = await ac.patch(
            f"/audits/{audit_id}/system-findings/{sf_id}/findings/Finding%20XYZ",
            json={"lifecycle_stage": "model_build"}
        )
        assert resp4.status_code == 404

    app.dependency_overrides.clear()
