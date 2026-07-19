import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, async_session_maker
from models.organization import Organization
from models.billing import BillingPlan, Subscription
from billing.service import get_org_subscription_status
from billing.schemas import SubscriptionStatus

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

@pytest.mark.asyncio
async def test_get_org_subscription_status_with_plan(db_session: AsyncSession):
    # Setup test data
    org = Organization(name="Test Org", slug=f"test-org-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.flush()

    plan = BillingPlan(
        name="pro",
        price_monthly=99,
        max_audits_per_month=10,
        max_users=5,
        features={"feature1": True}
    )
    db_session.add(plan)
    await db_session.flush()

    sub = Subscription(
        org_id=org.id,
        plan_id=plan.id,
        status="active"
    )
    db_session.add(sub)
    await db_session.commit()

    # Run function
    status = await get_org_subscription_status(db_session, org.id)

    # Verify result
    assert isinstance(status, SubscriptionStatus)
    assert status.tier == "pro"
    assert status.max_audits_per_month == 10
    assert status.max_users == 5
    assert status.max_ai_systems is None
    assert status.features == {"feature1": True}

@pytest.mark.asyncio
async def test_get_org_subscription_status_without_plan(db_session: AsyncSession, caplog):
    # Setup test data
    org = Organization(name="Test Org", slug=f"test-org-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()

    # Run function
    status = await get_org_subscription_status(db_session, org.id)

    # Verify result fallback
    assert isinstance(status, SubscriptionStatus)
    assert status.tier == "starter"
    assert status.max_audits_per_month == 1
    assert status.max_users == 1
    assert status.max_ai_systems is None
    assert status.features == {}

    # Verify log output
    assert f"Organization {org.id} has no assigned subscription plan" in caplog.text
