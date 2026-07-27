import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database import Base
import models
from models.audit import Audit
from organizations.service import OrganizationService
from models.organization import Organization
from models.user import User
from models.workflow import Workflow, WorkflowStatus
from models.engineering_record import EngineeringRecord
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
async def user(db_session: AsyncSession) -> User:
    ps = PasswordService()
    u = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password=ps.hash_password("password123")
    )
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)
    return u

@pytest_asyncio.fixture
async def organization(db_session: AsyncSession) -> Organization:
    org = Organization(name="Test Org")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest.mark.asyncio
async def test_operational_score_both_inputs(db_session, organization, user):
    # Setup
    workflow = Workflow(
        org_id=organization.id,
        user_id=user.id,
        status=WorkflowStatus.complete,
        input_config={},
        scores={"health": 80}
    )
    db_session.add(workflow)

    eng_record = EngineeringRecord(
        organization_id=organization.id,
        has_dedicated_ai_team=True, # 25
        has_mlops_pipeline=True, # 25
        # Total eng score = 50
    )
    db_session.add(eng_record)
    await db_session.commit()

    # Test
    service = OrganizationService(db_session)
    score_data = await service.get_operational_score(organization.id)

    assert score_data["is_partial"] is False
    assert score_data["missing_components"] == []
    # (80 + 50) / 2 = 65.0
    assert score_data["operational_score"] == 65.0

@pytest.mark.asyncio
async def test_operational_score_workflow_only(db_session, organization, user):
    workflow = Workflow(
        org_id=organization.id,
        user_id=user.id,
        status=WorkflowStatus.complete,
        input_config={},
        scores={"health": 90}
    )
    db_session.add(workflow)
    await db_session.commit()

    service = OrganizationService(db_session)
    score_data = await service.get_operational_score(organization.id)

    assert score_data["is_partial"] is True
    assert "engineering_score" in score_data["missing_components"]
    assert score_data["operational_score"] == 90.0

@pytest.mark.asyncio
async def test_operational_score_engineering_only(db_session, organization):
    eng_record = EngineeringRecord(
        organization_id=organization.id,
        has_dedicated_ai_team=True,
        has_mlops_pipeline=True,
    )
    db_session.add(eng_record)
    await db_session.commit()

    service = OrganizationService(db_session)
    score_data = await service.get_operational_score(organization.id)

    assert score_data["is_partial"] is True
    assert "workflow_health_score" in score_data["missing_components"]
    assert score_data["operational_score"] == 50.0

@pytest.mark.asyncio
async def test_operational_score_neither(db_session, organization):
    service = OrganizationService(db_session)
    score_data = await service.get_operational_score(organization.id)

    assert score_data["is_partial"] is True
    assert "workflow_health_score" in score_data["missing_components"]
    assert "engineering_score" in score_data["missing_components"]
    assert score_data["operational_score"] is None
    assert score_data["score_unavailable_reason"] == "No Workflow or Engineering Intelligence records found for this organization."

@pytest.mark.asyncio
async def test_operational_score_multiple_workflows(db_session, organization, user):
    # Complete, valid score
    w1 = Workflow(org_id=organization.id, user_id=user.id, status=WorkflowStatus.complete, input_config={}, scores={"health": 60})
    # Complete, valid score
    w2 = Workflow(org_id=organization.id, user_id=user.id, status=WorkflowStatus.complete, input_config={}, scores={"health": 100})
    # Failed, should be ignored
    w3 = Workflow(org_id=organization.id, user_id=user.id, status=WorkflowStatus.failed, input_config={}, scores={"health": 10})
    # Complete but missing health score, should be ignored from average
    w4 = Workflow(org_id=organization.id, user_id=user.id, status=WorkflowStatus.complete, input_config={}, scores={"other": 50})

    db_session.add_all([w1, w2, w3, w4])
    await db_session.commit()

    service = OrganizationService(db_session)
    score_data = await service.get_operational_score(organization.id)

    # Average of 60 and 100 = 80
    assert score_data["is_partial"] is True
    assert score_data["operational_score"] == 80.0
