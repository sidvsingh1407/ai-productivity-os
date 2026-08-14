import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from tests.test_ai_systems import db_session, setup_db
from models.organization import Organization
from models.ai_system import AISystem
from models.opportunity import Opportunity
from models.agent_recommendation import AgentRecommendation
from models.workflow_recommendation import WorkflowRecommendation
from models.roadmap_item import RoadmapItem
from roadmaps.engine import generate_investment_roadmap_items

@pytest.fixture
def org_id():
    return uuid.uuid4()

@pytest.mark.asyncio
async def test_investment_roadmap_no_cost(db_session: AsyncSession, org_id):
    org = Organization(id=org_id, name="Test Org")
    db_session.add(org)

    system = AISystem(id=uuid.uuid4(), organization_id=org_id, name="Test System")
    db_session.add(system)

    opp = Opportunity(
        id=uuid.uuid4(),
        organization_id=org_id,
        ai_system_id=system.id,
        category="Test",
        title="Opp",
        description="Opp Desc",
        source_module="Test",
        confidence_or_priority="High"
    )
    db_session.add(opp)

    await db_session.commit()

    items = await generate_investment_roadmap_items(db_session, org_id)
    assert len(items) == 0

@pytest.mark.asyncio
async def test_investment_roadmap_with_cost_partial(db_session: AsyncSession, org_id):
    org = Organization(id=org_id, name="Test Org")
    db_session.add(org)

    system = AISystem(
        id=uuid.uuid4(),
        organization_id=org_id,
        name="Test System",
        licensing_cost=1000.0,
        cloud_cost=None,
        inference_cost=None,
        maintenance_cost=None
    )
    db_session.add(system)

    opp = Opportunity(
        id=uuid.uuid4(),
        organization_id=org_id,
        ai_system_id=system.id,
        category="Test",
        title="Opp",
        description="Opp Desc",
        source_module="Test",
        confidence_or_priority="High"
    )
    db_session.add(opp)

    await db_session.commit()

    items = await generate_investment_roadmap_items(db_session, org_id)
    assert len(items) == 1
    assert items[0].category == "investment"
    assert "partial cost data" in items[0].description
    assert "cloud_cost" in items[0].description

@pytest.mark.asyncio
async def test_investment_roadmap_all_sources(db_session: AsyncSession, org_id):
    org = Organization(id=org_id, name="Test Org")
    db_session.add(org)

    system = AISystem(
        id=uuid.uuid4(),
        organization_id=org_id,
        name="Test System",
        licensing_cost=100.0,
        cloud_cost=100.0,
        inference_cost=100.0,
        maintenance_cost=100.0
    )
    db_session.add(system)

    opp = Opportunity(
        id=uuid.uuid4(),
        organization_id=org_id,
        ai_system_id=system.id,
        category="Test",
        title="Opp Title",
        description="Opp Desc",
        source_module="Test",
        confidence_or_priority="High"
    )
    db_session.add(opp)

    ar = AgentRecommendation(
        id=uuid.uuid4(),
        organization_id=org_id,
        opportunity_id=opp.id,
        agent_type="Agent Type",
        rationale="Agent Rationale",
        confidence="Medium"
    )
    db_session.add(ar)

    wr = WorkflowRecommendation(
        id=uuid.uuid4(),
        organization_id=org_id,
        opportunity_id=opp.id,
        recommendation_type="Workflow Type",
        rationale="Workflow Rationale",
        confidence="Low"
    )
    db_session.add(wr)

    await db_session.commit()

    items = await generate_investment_roadmap_items(db_session, org_id)
    assert len(items) == 3

    categories = [i.category for i in items]
    assert all(c == "investment" for c in categories)

    horizons = {i.time_horizon for i in items}
    assert horizons == {"30_day", "90_day", "1_year"}

    assert not any("partial cost data" in i.description for i in items)
