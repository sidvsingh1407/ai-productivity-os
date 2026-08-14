import pytest
import uuid
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.roadmap_item import RoadmapItem
from models.ai_system import AISystem
from models.organization import Organization
from models.opportunity import Opportunity
from models.risk_classification import RiskClassification
from models.dependency_map import DependencyNode, DependencyEdge
from roadmaps.engine import generate_governance_roadmap_items
from database import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# We will use an in-memory db specifically configured with Base.metadata.create_all
# to avoid OperationalError about missing tables in case standard db_session isn't
# setting it up right for this test file.

@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture
async def organization(db_session: AsyncSession):
    org_id = uuid.uuid4()
    org = Organization(id=org_id, name="Gov Test Org", slug="gov-test-org")
    db_session.add(org)
    await db_session.commit()
    return org

@pytest_asyncio.fixture
async def system_with_risk_and_deps(db_session: AsyncSession, organization: Organization):
    sys_id = uuid.uuid4()
    sys = AISystem(id=sys_id, organization_id=organization.id, name="Risky System", status="active", decision_making_role="not_specified")
    db_session.add(sys)
    await db_session.commit()

    # Add risk classification
    rc_id = uuid.uuid4()
    # mock audit_id
    audit_id = uuid.uuid4()
    rc = RiskClassification(
        id=rc_id, ai_system_id=sys.id, audit_id=audit_id, risk_level="unacceptable", rationale="bad", citation_reference="test"
    )
    db_session.add(rc)

    # Add dependencies
    node = DependencyNode(organization_id=organization.id, ai_system_id=sys.id, node_type="ai_system")
    db_session.add(node)
    await db_session.commit()

    for i in range(5):
        other_sys = AISystem(id=uuid.uuid4(), organization_id=organization.id, name=f"Other {i}", status="active", decision_making_role="not_specified")
        db_session.add(other_sys)
        await db_session.commit()

        other_node = DependencyNode(organization_id=organization.id, ai_system_id=other_sys.id, node_type="ai_system")
        db_session.add(other_node)
        await db_session.commit()

        edge = DependencyEdge(organization_id=organization.id, source_node_id=node.id, target_node_id=other_node.id, edge_type="depends_on")
        db_session.add(edge)

    await db_session.commit()

    return sys

@pytest.mark.asyncio
async def test_generate_governance_roadmap_items_creates_item(db_session: AsyncSession, organization: Organization, system_with_risk_and_deps: AISystem):
    # Need to add Phase 7 record (Opportunity)
    opp = Opportunity(
        organization_id=organization.id, ai_system_id=system_with_risk_and_deps.id, category="test", title="Test Opp", description="Test", source_module="test", confidence_or_priority="High"
    )
    db_session.add(opp)
    await db_session.commit()

    items = await generate_governance_roadmap_items(db_session, organization.id)

    assert len(items) == 1
    assert items[0].category == "governance"
    assert items[0].time_horizon == "30_day"
    assert items[0].opportunity_id == opp.id
    assert "unacceptable" in items[0].description
    assert "5" in items[0].description

@pytest.mark.asyncio
async def test_generate_governance_roadmap_items_skips_minimal_risk(db_session: AsyncSession, organization: Organization, system_with_risk_and_deps: AISystem):
    # Update risk to minimal
    rc = (await db_session.execute(select(RiskClassification).where(RiskClassification.ai_system_id == system_with_risk_and_deps.id))).scalar_one()
    rc.risk_level = "minimal_risk"
    await db_session.commit()

    items = await generate_governance_roadmap_items(db_session, organization.id)
    assert len(items) == 0

@pytest.mark.asyncio
async def test_generate_governance_roadmap_items_skips_low_dependency(db_session: AsyncSession, organization: Organization, system_with_risk_and_deps: AISystem):
    # Delete an edge to make it 4
    edges = (await db_session.execute(select(DependencyEdge))).scalars().all()
    await db_session.delete(edges[0])
    await db_session.commit()

    items = await generate_governance_roadmap_items(db_session, organization.id)
    assert len(items) == 0

@pytest.mark.asyncio
async def test_generate_governance_roadmap_items_skips_no_phase_7_record(db_session: AsyncSession, organization: Organization, system_with_risk_and_deps: AISystem):
    # Ensure there is no Opportunity
    opps = (await db_session.execute(select(Opportunity))).scalars().all()
    for opp in opps:
        await db_session.delete(opp)
    await db_session.commit()

    items = await generate_governance_roadmap_items(db_session, organization.id)
    assert len(items) == 0
