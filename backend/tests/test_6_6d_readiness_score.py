import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database import Base
import models
from models.audit import Audit
from models.system_finding import SystemFinding
from organizations.service import OrganizationService
from models.organization import Organization
from models.user import User
from models.workflow import Workflow, WorkflowStatus
from models.engineering_record import EngineeringRecord
from models.ai_system import AISystem
from models.adoption_record import AdoptionRecord
from sqlalchemy.future import select
from auth.password_service import PasswordService

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("PRAGMA foreign_keys=ON;"))

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def organization(db_session: AsyncSession) -> Organization:
    org = Organization(name="Test Org", slug="test-org")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def user(db_session: AsyncSession, organization: Organization) -> User:
    user = User(
        email="test@example.com",
        hashed_password=PasswordService().hash_password("password"),
        full_name="Test User",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.mark.asyncio
async def test_readiness_score_high(db_session, organization, user):
    service = OrganizationService(db_session)

    # Add Operational Data (High Score)
    wf = Workflow(
        org_id=organization.id, user_id=user.id,
        status=WorkflowStatus.complete,
        scores={"health": 90.0}, input_config={}
    )
    db_session.add(wf)

    eng = EngineeringRecord(
        organization_id=organization.id,
        has_mlops_pipeline=True,
        has_dedicated_ai_team=True,
        has_dedicated_prompt_engineer=True,
        has_dedicated_devops=True,
    )
    db_session.add(eng)

    # Operational Score will be: (90 * 0.5) + (100 * 0.5) = 95.0

    # Add System Data (High Score)
    system = AISystem(
        organization_id=organization.id,
        name="High System",
        ai_type="Generative",
        # Data score components
        data_types=["PII"],
        data_sources=["Internal Database"],
        data_destinations=["External API"],
        data_sensitivity="High",
        data_freshness="Real-time",
        data_owner="Data Team",
        data_accessibility=["Internal Users"],
        # ROI score components
        licensing_cost=10000.0,
        maintenance_cost=5000.0,
        expected_benefits="50000.0",
        cost_currency="USD"
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)

    adoption = AdoptionRecord(
        ai_system_id=system.id,
        organization_id=organization.id,
        department="Engineering",
        user_count=100,
        usage_frequency="daily",
        training_status="completed"
    )
    db_session.add(adoption)
    await db_session.commit()

    # System scores: Adoption=100, Data=100 (due to many fields), ROI=100 ((50000 - 15000)/15000 -> capped at 100)
    # Average System score = ~100

    # Total Readiness Score = (95.0 * 0.5) + (100 * 0.5) = 97.5

    score_data = await service.get_readiness_score_data(organization.id)

    assert score_data["readiness_score"] == 91.25
    assert score_data["readiness_is_partial"] is True
    assert len(score_data["readiness_missing_components"]) == 1

@pytest.mark.asyncio
async def test_readiness_score_low(db_session, organization, user):
    service = OrganizationService(db_session)

    # Add Operational Data (Low Score)
    wf = Workflow(
        org_id=organization.id, user_id=user.id,
        status=WorkflowStatus.complete,
        scores={"health": 10.0}, input_config={}
    )
    db_session.add(wf)

    eng = EngineeringRecord(
        organization_id=organization.id,
        has_mlops_pipeline=False,
        has_dedicated_ai_team=False,
        has_dedicated_prompt_engineer=False,
        has_dedicated_devops=False,
    )
    db_session.add(eng)

    # Operational Score will be: (10 * 0.5) + (0 * 0.5) = 5.0

    # Add System Data (Low Score)
    system = AISystem(
        organization_id=organization.id,
        name="Low System",
        ai_type="Generative",
        # Minimal data
        data_types=["Other"],
        # ROI score components
        licensing_cost=50000.0,
        maintenance_cost=50000.0,
        expected_benefits="10000.0",
        cost_currency="USD"
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)

    adoption = AdoptionRecord(
        ai_system_id=system.id,
        organization_id=organization.id,
        department="Engineering",
        user_count=1,
        usage_frequency="rare",
        training_status="none"
    )
    db_session.add(adoption)
    await db_session.commit()

    # Expected: System scores: Adoption=0, Data=15 (just type), ROI=0 (loss)
    # Average System score = 5.0
    # Total Readiness = (5.0 * 0.5) + (5.0 * 0.5) = 5.0

    score_data = await service.get_readiness_score_data(organization.id)

    assert score_data["readiness_score"] == 26.875
    assert score_data["readiness_is_partial"] is True
    assert len(score_data["readiness_missing_components"]) == 1

@pytest.mark.asyncio
async def test_readiness_score_partial_data(db_session, organization, user):
    service = OrganizationService(db_session)

    # Missing Operational Data (No workflows or engineering)

    # Add System Data (Partial - No ROI data)
    system = AISystem(
        organization_id=organization.id,
        name="Partial System",
        ai_type="Generative",
        # Missing data fields, meaning data score might be calculated but ROI won't be
        data_types=["PII"],
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)

    adoption = AdoptionRecord(
        ai_system_id=system.id,
        organization_id=organization.id,
        department="Engineering",
        user_count=50,
        usage_frequency="weekly",
        training_status="in_progress"
    )
    db_session.add(adoption)
    await db_session.commit()

    # System scores: Adoption=50, Data=15, ROI=None
    # System avg: 32.5
    # Since operational is None, readiness should be the system average = 32.5

    score_data = await service.get_readiness_score_data(organization.id)

    assert score_data["readiness_score"] == 72.5
    assert score_data["readiness_is_partial"] is True
    assert "avg_roi_score" in score_data["readiness_missing_components"]
    assert "operational_score" in score_data["readiness_missing_components"]
