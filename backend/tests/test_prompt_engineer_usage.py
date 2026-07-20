import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.prompt_engineer_subscription import PromptEngineerSubscription
from prompt_engineer_usage.service import PromptEngineerUsageService
from prompt_engineer_usage.schemas import PromptEngineerUsageCreate


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
async def organization2(db_session: AsyncSession):
    org = Organization(name="Test Org 2", slug=f"test-org2-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def subscription(db_session: AsyncSession, organization: Organization):
    sub = PromptEngineerSubscription(organization_id=organization.id)
    db_session.add(sub)
    await db_session.commit()
    await db_session.refresh(sub)
    return sub

@pytest_asyncio.fixture
async def subscription2(db_session: AsyncSession, organization2: Organization):
    sub = PromptEngineerSubscription(organization_id=organization2.id)
    db_session.add(sub)
    await db_session.commit()
    await db_session.refresh(sub)
    return sub

@pytest.mark.asyncio
async def test_create_usage_record(db_session: AsyncSession, organization: Organization, subscription: PromptEngineerSubscription):
    service = PromptEngineerUsageService()

    usage_data = PromptEngineerUsageCreate(
        subscription_id=subscription.id,
        usage_type="prompt_generation",
        token_count=150,
        request_count=1,
        model_used="claude-sonnet-4-6"
    )

    usage_record = await service.log_usage(db_session, organization.id, usage_data)

    assert usage_record.id is not None
    assert usage_record.organization_id == organization.id
    assert usage_record.subscription_id == subscription.id
    assert usage_record.usage_type == "prompt_generation"
    assert usage_record.token_count == 150
    assert usage_record.request_count == 1
    assert usage_record.model_used == "claude-sonnet-4-6"
    assert usage_record.created_at is not None

@pytest.mark.asyncio
async def test_list_usage_records_scoped_to_organization_id(db_session: AsyncSession, organization: Organization, organization2: Organization, subscription: PromptEngineerSubscription, subscription2: PromptEngineerSubscription):
    service = PromptEngineerUsageService()

    # Create usage for org 1
    usage_data_1 = PromptEngineerUsageCreate(
        subscription_id=subscription.id,
        usage_type="prompt_generation"
    )
    await service.log_usage(db_session, organization.id, usage_data_1)

    # Create usage for org 2
    usage_data_2 = PromptEngineerUsageCreate(
        subscription_id=subscription2.id,
        usage_type="prompt_improvement"
    )
    await service.log_usage(db_session, organization2.id, usage_data_2)

    # List usage for org 1
    org_1_usage = await service.list_usage(db_session, organization.id)
    assert len(org_1_usage) == 1
    assert org_1_usage[0].organization_id == organization.id
    assert org_1_usage[0].usage_type == "prompt_generation"

    # List usage for org 2
    org_2_usage = await service.list_usage(db_session, organization2.id)
    assert len(org_2_usage) == 1
    assert org_2_usage[0].organization_id == organization2.id
    assert org_2_usage[0].usage_type == "prompt_improvement"

    # Org 1 cannot see Org 2's usage
    assert org_2_usage[0].id not in [u.id for u in org_1_usage]

def test_usage_records_cannot_be_updated_or_deleted():
    service = PromptEngineerUsageService()

    # Verify that the service does not have update or delete methods
    assert not hasattr(service, "update_usage"), "Service should not have an update_usage method"
    assert not hasattr(service, "delete_usage"), "Service should not have a delete_usage method"
    assert not hasattr(service, "update"), "Service should not have an update method"
    assert not hasattr(service, "delete"), "Service should not have a delete method"
