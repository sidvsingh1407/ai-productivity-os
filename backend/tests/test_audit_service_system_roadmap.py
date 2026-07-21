import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, async_session_maker
from models.organization import Organization
from models.ai_system import AISystem
from models.audit import Audit
from models.user import User
from models.risk_classification import RiskClassification
from models.monitoring_plan import MonitoringPlan

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
    user = User(email=f"test{uuid.uuid4().hex[:8]}@example.com", full_name="Test User", hashed_password="pw")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.mark.asyncio
async def test_run_audit_roadmap_synthesis(db_session: AsyncSession, organization: Organization, user: User, mocker):
    sys1 = AISystem(organization_id=organization.id, name="High Risk Sys", data_types=["personal"], decision_making_role="automated", status="active", criticality="high")
    sys2 = AISystem(organization_id=organization.id, name="Low Risk Sys", data_types=["public"], decision_making_role="advisor", status="active", criticality="low")
    db_session.add_all([sys1, sys2])
    await db_session.commit()
    await db_session.refresh(sys1)
    await db_session.refresh(sys2)

    mock_risk1 = RiskClassification(audit_id=uuid.uuid4(), ai_system_id=sys1.id, risk_level="High Risk", rationale="", citation_reference="")
    mock_risk2 = RiskClassification(audit_id=uuid.uuid4(), ai_system_id=sys2.id, risk_level="Low Risk", rationale="", citation_reference="")

    mock_plan1 = MonitoringPlan(organization_id=organization.id, ai_system_id=sys1.id, review_cadence="monthly", monitoring_scope=[])

    mocker.patch('audits.repository.get_risk_classifications_by_audit', return_value=[mock_risk1, mock_risk2])
    mocker.patch('audits.repository.get_monitoring_plans_by_systems', return_value=[mock_plan1])

    mock_intel = {
        "findings": [],
        "recommendations": [
            {"recommendation": "Rec High", "priority": "Immediate", "expected_impact": "impact", "implementation_effort": "high"},
            {"recommendation": "Rec Low", "priority": "Long-Term", "expected_impact": "impact", "implementation_effort": "high"}
        ],
        "executive_summary": {
            "overall_assessment": "",
            "critical_risk": "",
            "primary_opportunity": "",
            "recommended_first_action": ""
        },
        "target_state": [],
        "dashboard": {
            "critical_risk": "", "priority_action": "", "improvement_opportunity": "", "executive_summary": ""
        },
        "risk_projection": {
            "risk_level": "High", "risk_score": 100, "risk_trend": "", "confidence": 100, "explanation": "", "risk_drivers": [], "risk_timeline": {"near_term": [], "mid_term": [], "long_term": []}
        }
    }
    mocker.patch('audits.service.generate_intelligence', return_value=mock_intel)

    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    result = await run_audit(db_session, organization.id, user.id, form_response)

    roadmap = result.intelligence.roadmap
    assert roadmap is not None

    actions_30 = [a.action for a in roadmap.day_30]
    actions_90 = [a.action for a in roadmap.day_90]

    print("Actions 30:", actions_30)
    print("Actions 90:", actions_90)

    # Immediate priority maps to day_30 for both systems
    assert any("[High Risk Sys] Rec High" in a for a in actions_30)
    assert any("(Monitored monthly)" in a for a in actions_30)
    assert any("[Low Risk Sys] Rec High" in a for a in actions_30)

    # Long-Term priority maps to day_90 for both systems
    assert any("[High Risk Sys] Rec Low" in a for a in actions_90)
    assert any("[Low Risk Sys] Rec Low" in a for a in actions_90)

@pytest.mark.asyncio
async def test_run_audit_roadmap_missing_monitoring(db_session: AsyncSession, organization: Organization, user: User, mocker):
    sys1 = AISystem(organization_id=organization.id, name="Sys Without Plan", data_types=["personal"], decision_making_role="automated", status="active", criticality="high")
    db_session.add_all([sys1])
    await db_session.commit()
    await db_session.refresh(sys1)

    mock_risk1 = RiskClassification(audit_id=uuid.uuid4(), ai_system_id=sys1.id, risk_level="Medium", rationale="", citation_reference="")

    mocker.patch('audits.repository.get_risk_classifications_by_audit', return_value=[mock_risk1])
    mocker.patch('audits.repository.get_monitoring_plans_by_systems', return_value=[])

    mock_intel = {
        "findings": [],
        "recommendations": [
            {"recommendation": "Rec No Priority", "priority": "", "expected_impact": "impact", "implementation_effort": "high"}
        ],
        "executive_summary": {
            "overall_assessment": "",
            "critical_risk": "",
            "primary_opportunity": "",
            "recommended_first_action": ""
        },
        "target_state": [],
        "dashboard": {
            "critical_risk": "", "priority_action": "", "improvement_opportunity": "", "executive_summary": ""
        },
        "risk_projection": {
            "risk_level": "High", "risk_score": 100, "risk_trend": "", "confidence": 100, "explanation": "", "risk_drivers": [], "risk_timeline": {"near_term": [], "mid_term": [], "long_term": []}
        }
    }
    mocker.patch('audits.service.generate_intelligence', return_value=mock_intel)

    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }

    result = await run_audit(db_session, organization.id, user.id, form_response)
    roadmap = result.intelligence.roadmap

    # Risk is "Medium" so it goes to day_60
    actions_60 = [a.action for a in roadmap.day_60]
    assert any("[Sys Without Plan] Rec No Priority" in a for a in actions_60)
    assert not any("(Monitored" in a for a in actions_60)

@pytest.mark.asyncio
async def test_roadmap_engine_priority_precedence():
    from audits.roadmap_engine import generate_system_driven_roadmap

    system_findings = [
        {
            "ai_system_id": "sys-a",
            "ai_system_name": "System A",
            "recommendations": [
                {
                    "recommendation": "Urgent patch needed",
                    "priority": "Critical"
                }
            ]
        },
        {
            "ai_system_id": "sys-b",
            "ai_system_name": "System B",
            "recommendations": [
                {
                    "recommendation": "Update docs",
                    "priority": "Medium"
                }
            ]
        }
    ]

    risk_classes = {
        "sys-a": "Low",
        "sys-b": "High"
    }

    res = generate_system_driven_roadmap(system_findings, risk_classes, {})
    roadmap = res["roadmap"]

    day_30_actions = [a["action"] for a in roadmap["day_30"]]
    assert any("[System A]" in a for a in day_30_actions)

    day_60_actions = [a["action"] for a in roadmap["day_60"]]
    assert any("[System B]" in a for a in day_60_actions)
