import pytest
import pytest_asyncio
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, async_session_maker
from models.monitoring_plan import MonitoringPlan
from models.organization import Organization
from models.ai_system import AISystem
from models.user import User
from models.audit import Audit

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
async def setup_organization(db_session: AsyncSession):
    org = Organization(name="Test Org", slug=f"test-org-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def setup_ai_system(db_session: AsyncSession, setup_organization: Organization):
    system = AISystem(
        organization_id=setup_organization.id,
        name="Test System",
        purpose="Testing",
        data_types=["test"]
    )
    db_session.add(system)
    await db_session.commit()
    await db_session.refresh(system)
    return system

@pytest.mark.asyncio
async def test_monitoring_plan_creation_success(db_session, setup_organization, setup_ai_system):
    # Setup test data using existing fixtures
    organization = setup_organization
    ai_system = setup_ai_system

    # Create MonitoringPlan with valid FKs
    new_plan = MonitoringPlan(
        organization_id=organization.id,
        ai_system_id=ai_system.id,
        status="active",
        monitoring_scope=[{"finding_id": "test"}]
    )

    db_session.add(new_plan)
    await db_session.commit()
    await db_session.refresh(new_plan)

    assert new_plan.id is not None
    assert new_plan.organization_id == organization.id
    assert new_plan.ai_system_id == ai_system.id
    assert new_plan.status == "active"
    assert new_plan.monitoring_scope == [{"finding_id": "test"}]
    assert new_plan.created_at is not None
    assert new_plan.updated_at is not None

@pytest.mark.asyncio
async def test_monitoring_plan_creation_invalid_fks(db_session):
    # Create MonitoringPlan with invalid FKs
    invalid_plan = MonitoringPlan(
        organization_id=uuid.uuid4(),  # Random UUID, does not exist in DB
        ai_system_id=uuid.uuid4(),     # Random UUID, does not exist in DB
        status="draft",
        monitoring_scope=[]
    )

    db_session.add(invalid_plan)

    # Ensure SQLite enforces foreign keys for this connection
    from sqlalchemy import text
    await db_session.execute(text("PRAGMA foreign_keys=ON;"))

    with pytest.raises(IntegrityError):
        await db_session.commit()
