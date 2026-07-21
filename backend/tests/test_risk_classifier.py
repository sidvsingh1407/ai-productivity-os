import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from models.ai_system import AISystem
from models.audit import Audit
from models.system_finding import SystemFinding
from models.risk_classification import RiskClassification
from audits.risk_classifier import classify_system

@pytest.fixture
def mock_db_session(mocker):
    session = mocker.Mock(spec=AsyncSession)
    return session

@pytest.fixture
def mock_regulation_service(mocker):
    from citations.schemas import Citation
    from regulation.schemas import SearchResponseItem
    mocker.patch('audits.risk_classifier.RegulationService.search', return_value=[
        SearchResponseItem(chunk_text="mock chunk", article_number="5", section_title="prohibited", relevance_score=1.0)
    ])
    mocker.patch('audits.risk_classifier.CitationFormatterService.format_citations', return_value=[
        Citation(chunk_text="mock chunk", citation="Mock Citation", relevance_score=1.0)
    ])
    return True

@pytest.mark.asyncio
async def test_classify_unacceptable_risk(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Social Scoring AI",
        purpose="social scoring for public authorities",
        data_types=["demographic data"],
        decision_making_role="fully automated",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))

    assert result.risk_level == "unacceptable"
    assert result.requires_human_review is False
    assert result.matched_category is None
    assert result.citation_reference == "Mock Citation"

@pytest.mark.asyncio
async def test_classify_high_risk_domain(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="HR Hiring System",
        purpose="AI system for employee recruitment and worker management",
        data_types=["resumes", "interview transcripts"],
        decision_making_role="human in the loop",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))

    assert result.risk_level == "high_risk"
    assert result.matched_category == "employment/worker management"
    assert result.requires_human_review is False

@pytest.mark.asyncio
async def test_classify_ambiguous_risk(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Vague System",
        purpose="tools",
        data_types=[],
        decision_making_role="unknown",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))

    assert result.risk_level == "ambiguous"
    assert result.requires_human_review is True

@pytest.mark.asyncio
async def test_classify_escalated_high_risk(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Automated Pricing API",
        purpose="dynamic pricing API based on personal data",
        data_types=["location", "demographic", "financial data"],
        decision_making_role="fully automated with no human review",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))

    assert result.risk_level == "high_risk"
    assert result.matched_category is None
    assert result.requires_human_review is False
    assert "processes personal data and utilizes fully automated decision making" in result.rationale

@pytest.mark.asyncio
async def test_classify_minimal_risk(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Internal Analytics",
        purpose="generate aggregate charts from system logs",
        data_types=["server metrics", "API latency data"],
        decision_making_role="advisory dashboard",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))

    assert result.risk_level == "minimal_risk"
    assert result.requires_human_review is False

@pytest.mark.asyncio
async def test_classification_reproducibility(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Credit Scoring Tool",
        purpose="evaluate credit worthiness for essential services",
        data_types=["financial history"],
        decision_making_role="human in the loop",
        status="active"
    )
    audit_id = str(uuid.uuid4())

    result1 = await classify_system(system, mock_db_session, audit_id)
    result2 = await classify_system(system, mock_db_session, audit_id)

    assert result1.risk_level == result2.risk_level
    assert result1.matched_category == result2.matched_category
    assert result1.rationale == result2.rationale
    assert result1.requires_human_review == result2.requires_human_review

@pytest.mark.asyncio
async def test_classify_unacceptable_risk_compound_biometric(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Police Tracker",
        purpose="real-time remote biometric identification in publicly accessible space",
        data_types=["faces"],
        decision_making_role="fully automated",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))
    assert result.risk_level == "unacceptable"

@pytest.mark.asyncio
async def test_classify_unacceptable_risk_compound_exploitation(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Predatory AI",
        purpose="exploitation of vulnerabilities based on socioeconomic status",
        data_types=["data"],
        decision_making_role="fully automated",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))
    assert result.risk_level == "unacceptable"

@pytest.mark.asyncio
async def test_classify_high_risk_law_enforcement_legit(mock_db_session, mock_regulation_service):
    system = AISystem(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        name="Standard Police Database",
        purpose="case management for law enforcement",
        data_types=["case notes"],
        decision_making_role="advisor",
        status="active"
    )

    result = await classify_system(system, mock_db_session, str(uuid.uuid4()))
    assert result.risk_level == "high_risk"
    assert result.matched_category == "law enforcement"
