import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from models.organization import Organization
from models.opportunity import Opportunity
from models.agent_recommendation import AgentRecommendation
from agent_recommendations import service
import uuid
import pytest_asyncio
from database import engine, Base, async_session_maker
import models  # loads all models into Base.metadata

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

@pytest.mark.asyncio
async def test_list_agent_recommendations_filter(db_session: AsyncSession, organization: Organization):
    org = organization
    opp_id1 = uuid.uuid4()
    opp_id2 = uuid.uuid4()

    # insert opps first
    opp1 = Opportunity(id=opp_id1, organization_id=org.id, category="manual_work", title="T1", description="D1", source_module="s1", confidence_or_priority="High")
    opp2 = Opportunity(id=opp_id2, organization_id=org.id, category="customer_pain", title="T2", description="D2", source_module="s2", confidence_or_priority="High")
    db_session.add_all([opp1, opp2])
    await db_session.commit()

    rec1 = AgentRecommendation(organization_id=org.id, opportunity_id=opp_id1, agent_type="hr_agent", rationale="R1", confidence="High")
    rec2 = AgentRecommendation(organization_id=org.id, opportunity_id=opp_id2, agent_type="customer_support_agent", rationale="R2", confidence="Medium")
    db_session.add_all([rec1, rec2])
    await db_session.commit()

    # filter by opportunity_id
    res_opp = await service.list_agent_recommendations(db_session, org.id, opportunity_id=opp_id1)
    assert res_opp["total"] == 1
    assert res_opp["items"][0].agent_type == "hr_agent"

    # filter by agent_type
    res_agent = await service.list_agent_recommendations(db_session, org.id, agent_type="customer_support_agent")
    assert res_agent["total"] == 1
    assert res_agent["items"][0].agent_type == "customer_support_agent"
    assert res_agent["items"][0].opportunity_id == opp_id2
