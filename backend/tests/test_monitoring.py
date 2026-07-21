import pytest
import pytest_asyncio
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import engine, Base, async_session_maker
from models.organization import Organization
from models.ai_system import AISystem
from models.audit import Audit, AuditStatus
from models.monitoring_plan import MonitoringPlan
from models.monitoring_check_result import MonitoringCheckResult
from monitoring.service import run_due_monitoring_checks, _calculate_next_run_at

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
async def test_org(db_session: AsyncSession):
    org = Organization(name="Test Org Monitoring", slug=f"test-org-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def test_ai_system(db_session: AsyncSession, test_org: Organization):
    system = AISystem(
        organization_id=test_org.id,
        name="Test Monitoring System",
        criticality="High",
        ai_type="Generative",
        decision_making_role="autonomous",
        data_types=["PII"]
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)
    return system

@pytest_asyncio.fixture
async def test_audit(db_session: AsyncSession, test_org: Organization, test_ai_system: AISystem):
    audit = Audit(
        org_id=test_org.id,
        user_id=uuid.uuid4(),
        status=AuditStatus.complete,
        scores={"dimensions": {"governance": 10, "integration": 10}},
        form_response={"companyName": "Test"},
        industry_type="FINTECH"
    )
    db_session.add(audit)
    await db_session.commit()
    await db_session.refresh(audit)
    return audit

@pytest.mark.asyncio
async def test_monitoring_execution_picks_up_due_plan(db_session: AsyncSession, test_org: Organization, test_ai_system: AISystem, test_audit: Audit):
    now = datetime.now(timezone.utc)
    past_date = now - timedelta(days=2)

    plan = MonitoringPlan(
        organization_id=test_org.id,
        ai_system_id=test_ai_system.id,
        status="active",
        monitoring_scope=[],
        review_cadence="daily",
        next_run_at=past_date
    )
    db_session.add(plan)
    await db_session.commit()
    await db_session.refresh(plan)

    # Run background check
    await run_due_monitoring_checks(async_session_maker)

    # Refresh plan to check if it was updated
    await db_session.refresh(plan)

    assert plan.last_reviewed_at is not None

    # SQLite drops timezone info, handle comparison gracefully
    if plan.next_run_at.tzinfo is None:
        assert plan.next_run_at > now.replace(tzinfo=None)
    else:
        assert plan.next_run_at > now

    # Check if MonitoringCheckResult was created
    stmt = select(MonitoringCheckResult).where(MonitoringCheckResult.monitoring_plan_id == plan.id)
    result = await db_session.execute(stmt)
    check_result = result.scalar_one_or_none()

    assert check_result is not None
    assert check_result.ai_system_id == test_ai_system.id
    assert isinstance(check_result.findings, list)

@pytest.mark.asyncio
async def test_monitoring_execution_ignores_not_due_plan(db_session: AsyncSession, test_org: Organization, test_ai_system: AISystem):
    now = datetime.now(timezone.utc)
    future_date = now + timedelta(days=2)

    plan = MonitoringPlan(
        organization_id=test_org.id,
        ai_system_id=test_ai_system.id,
        status="active",
        monitoring_scope=[],
        review_cadence="daily",
        next_run_at=future_date
    )
    db_session.add(plan)
    await db_session.commit()
    await db_session.refresh(plan)

    # Run background check
    await run_due_monitoring_checks(async_session_maker)

    # Refresh plan to check if it was updated
    await db_session.refresh(plan)

    # Should be unmodified
    assert plan.last_reviewed_at is None

    # SQLite drops timezone info, so we compare without it if necessary
    if plan.next_run_at.tzinfo is None:
        assert plan.next_run_at == future_date.replace(tzinfo=None)
    else:
        assert plan.next_run_at == future_date

    # No check result should be created
    stmt = select(MonitoringCheckResult).where(MonitoringCheckResult.monitoring_plan_id == plan.id)
    result = await db_session.execute(stmt)
    assert result.scalar_one_or_none() is None

def test_calculate_next_run_at():
    now = datetime.now(timezone.utc)
    assert _calculate_next_run_at("daily", now) == now + timedelta(days=1)
    assert _calculate_next_run_at("weekly", now) == now + timedelta(weeks=1)
    assert _calculate_next_run_at("monthly", now) == now + timedelta(days=30)
    assert _calculate_next_run_at("invalid", now) == now + timedelta(days=1) # Fallback
