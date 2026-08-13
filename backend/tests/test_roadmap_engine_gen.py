import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import engine, Base, async_session_maker
from models.organization import Organization
from models.opportunity import Opportunity
from models.agent_recommendation import AgentRecommendation
from models.workflow_recommendation import WorkflowRecommendation
from models.roadmap_item import RoadmapItem

from roadmaps.engine import generate_roadmap_items

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
async def test_generate_roadmap_items_creates_all(db_session: AsyncSession):
    # Set up
    org_id = uuid.uuid4()
    org = Organization(id=org_id, name="Test Org", slug="test-org-gen")
    db_session.add(org)

    # 1. Opportunity
    opp_id = uuid.uuid4()
    opp = Opportunity(
        id=opp_id,
        organization_id=org_id,
        category="knowledge_bottleneck",
        title="Opp Title",
        description="Opp Desc",
        source_module="workflow",
        confidence_or_priority="High"
    )

    # 2. Agent Recommendation
    ar_id = uuid.uuid4()
    ar = AgentRecommendation(
        id=ar_id,
        organization_id=org_id,
        opportunity_id=opp_id,
        agent_type="support_agent",
        rationale="AR Rationale",
        confidence="Medium"
    )

    # 3. Workflow Recommendation
    wr_id = uuid.uuid4()
    wr = WorkflowRecommendation(
        id=wr_id,
        organization_id=org_id,
        opportunity_id=opp_id,
        recommendation_type="rag",
        rationale="WR Rationale",
        confidence="Low"
    )

    db_session.add_all([opp, ar, wr])
    await db_session.commit()

    # Call generate
    items = await generate_roadmap_items(db_session, org_id)
    await db_session.commit()

    assert len(items) == 3

    # Check DB
    stmt = select(RoadmapItem).where(RoadmapItem.organization_id == org_id)
    result = await db_session.execute(stmt)
    db_items = result.scalars().all()

    assert len(db_items) == 3

    opp_item = next(i for i in db_items if i.source_type == "opportunity")
    assert opp_item.opportunity_id == opp_id
    assert opp_item.time_horizon == "30_day"
    assert opp_item.title == "Opp Title"
    assert opp_item.description == "Opp Desc"
    assert opp_item.category == "general"

    ar_item = next(i for i in db_items if i.source_type == "agent_recommendation")
    assert ar_item.agent_recommendation_id == ar_id
    assert ar_item.time_horizon == "90_day"
    assert ar_item.title == "support_agent"
    assert ar_item.description == "AR Rationale"
    assert ar_item.category == "general"

    wr_item = next(i for i in db_items if i.source_type == "workflow_recommendation")
    assert wr_item.workflow_recommendation_id == wr_id
    assert wr_item.time_horizon == "1_year"
    assert wr_item.title == "rag"
    assert wr_item.description == "WR Rationale"
    assert wr_item.category == "general"


@pytest.mark.asyncio
async def test_generate_roadmap_items_skips_invalid_confidence(db_session: AsyncSession):
    org_id = uuid.uuid4()
    org = Organization(id=org_id, name="Test Org", slug="test-org-gen-2")
    db_session.add(org)

    opp_id = uuid.uuid4()
    opp = Opportunity(
        id=opp_id,
        organization_id=org_id,
        category="knowledge_bottleneck",
        title="Opp Title",
        description="Opp Desc",
        source_module="workflow",
        confidence_or_priority="UnknownPriority"
    )
    db_session.add(opp)
    await db_session.commit()

    items = await generate_roadmap_items(db_session, org_id)
    assert len(items) == 0

@pytest.mark.asyncio
async def test_generate_roadmap_items_idempotency(db_session: AsyncSession):
    org_id = uuid.uuid4()
    org = Organization(id=org_id, name="Test Org", slug="test-org-gen-3")
    db_session.add(org)

    opp_id = uuid.uuid4()
    opp = Opportunity(
        id=opp_id,
        organization_id=org_id,
        category="knowledge_bottleneck",
        title="Opp Title",
        description="Opp Desc",
        source_module="workflow",
        confidence_or_priority="High"
    )
    db_session.add(opp)
    await db_session.commit()

    # First run
    items_1 = await generate_roadmap_items(db_session, org_id)
    await db_session.commit()
    assert len(items_1) == 1

    # Let's add a fake 'other' category roadmap item to ensure it doesn't get deleted
    fake_item = RoadmapItem(
        organization_id=org_id,
        source_type="opportunity",
        opportunity_id=opp_id,
        category="investment",
        time_horizon="30_day",
        title="Investment",
        description="Investment Desc"
    )
    db_session.add(fake_item)
    await db_session.commit()

    # Second run
    items_2 = await generate_roadmap_items(db_session, org_id)
    await db_session.commit()
    assert len(items_2) == 1 # The new 'general' item

    # Total items for org should be 2: one 'general', one 'investment'
    stmt = select(RoadmapItem).where(RoadmapItem.organization_id == org_id)
    result = await db_session.execute(stmt)
    db_items = result.scalars().all()

    assert len(db_items) == 2
    assert {"general", "investment"} == {i.category for i in db_items}
