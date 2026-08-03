import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from models.organization import Organization
import uuid
from models.opportunity import Opportunity
from opportunities import service
import pytest_asyncio
from database import engine, Base, async_session_maker
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
async def organization(db_session: AsyncSession):
    org = Organization(name="Test Org", slug=f"test-org-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest.mark.asyncio
async def test_generate_opportunities(db_session: AsyncSession, organization: Organization):
    org = organization

    # We test the engine directly first
    from opportunities.engine import generate_opportunities

    # 1. Adoption (high resistance, no training) -> triggers customer_pain
    adoption_records = [{
        "ai_system_id": "00000000-0000-0000-0000-000000000001",
        "organization_id": org.id,
        "resistance_level": "high",
        "training_status": "none",
        "shadow_ai_detected": False
    }]

    # 2. Workflows (Heavy manual handoffs + bottleneck < 50) -> triggers automation_candidate
    workflows = [{
        "org_id": org.id,
        "scores": {"bottleneck": 30, "risk": 80},
        "findings": {"weaknesses": ["Heavy manual handoffs delay everything"]}
    }]

    # 3. AISystem (data intelligence, static/unknown + manual only) -> triggers knowledge_bottleneck
    ai_systems = [{
        "id": "00000000-0000-0000-0000-000000000001",
        "organization_id": org.id,
        "data_freshness": "static",
        "data_quality_notes": "very poor quality",
        "data_accessibility": ["manual_export", "email_attachment"]
    }]

    # 4. Engineering Intelligence (no MLOps, no monitoring) -> triggers department_pain
    engineering_records = [{
        "organization_id": org.id,
        "team_size": 2, # Must be > 0 to trigger
        "has_mlops_pipeline": False,
        "monitoring_tooling": []
    }]

    opps = generate_opportunities(
        adoption_records=adoption_records,
        workflows=workflows,
        ai_systems=ai_systems,
        engineering_records=engineering_records
    )

    # Asserting opportunities were generated correctly
    categories = [o["category"] for o in opps]
    assert len(opps) == 4
    assert "customer_pain" in categories
    assert "automation_candidate" in categories
    assert "knowledge_bottleneck" in categories
    assert "department_pain" in categories

@pytest.mark.asyncio
async def test_generate_opportunities_no_trigger_on_defaults(db_session: AsyncSession, organization: Organization):
    org = organization

    from opportunities.engine import generate_opportunities

    # Adoption: Default values should NOT trigger anything.
    adoption_records = [{
        "ai_system_id": "00000000-0000-0000-0000-000000000001",
        "organization_id": org.id,
        "resistance_level": "not_specified",
        "training_status": "not_specified",
        "shadow_ai_detected": False
    }]

    # Engineering: team_size = 0 (no team assumed) -> no trigger even if mlops is False
    engineering_records = [{
        "organization_id": org.id,
        "team_size": 0,
        "has_mlops_pipeline": False,
        "monitoring_tooling": []
    }]

    opps = generate_opportunities(
        adoption_records=adoption_records,
        workflows=[],
        ai_systems=[],
        engineering_records=engineering_records
    )

    assert len(opps) == 0

@pytest.mark.asyncio
async def test_list_opportunities_filter(db_session: AsyncSession, organization: Organization):
    # Tests the service list function (which is used by router)
    org = organization

    # Insert some fake opps
    import uuid
    from opportunities.repository import create_opportunity

    sys_id1 = uuid.uuid4()

    await create_opportunity(db_session, {
        "organization_id": org.id,
        "ai_system_id": sys_id1,
        "category": "manual_work",
        "title": "T1",
        "description": "D1",
        "source_module": "t",
        "confidence_or_priority": "High"
    })

    await create_opportunity(db_session, {
        "organization_id": org.id,
        "ai_system_id": None, # Org level
        "category": "department_pain",
        "title": "T2",
        "description": "D2",
        "source_module": "t",
        "confidence_or_priority": "High"
    })

    # filter by null_filter (org-level)
    res_null = await service.list_opportunities(db_session, org.id, ai_system_id="null")
    assert res_null["total"] == 1
    assert res_null["items"][0].category == "department_pain"

    # filter by sys_id
    res_sys = await service.list_opportunities(db_session, org.id, ai_system_id=str(sys_id1))
    assert res_sys["total"] == 1
    assert res_sys["items"][0].category == "manual_work"
