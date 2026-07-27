import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from database import engine, Base, async_session_maker
from models.organization import Organization, OrgMember, OrgRole
from models.ai_system import AISystem

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
async def user(db_session: AsyncSession, organization: Organization):
    from models.user import User
    u = User(email="test@example.com", full_name="Test User", hashed_password="fake")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)

    member = OrgMember(org_id=organization.id, user_id=u.id, role=OrgRole.admin)
    db_session.add(member)
    await db_session.commit()
    return u

# Fixtures for user and org
@pytest_asyncio.fixture
async def organization2(db_session: AsyncSession):
    org = Organization(name="Test Org 2", slug=f"test-org2-{uuid.uuid4().hex[:8]}")
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

@pytest_asyncio.fixture
async def user2(db_session: AsyncSession, organization2: Organization):
    from models.user import User
    u = User(email="test2@example.com", full_name="Test User 2", hashed_password="fake")
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)

    member = OrgMember(org_id=organization2.id, user_id=u.id, role=OrgRole.admin)
    db_session.add(member)
    await db_session.commit()
    return u

@pytest.fixture
def system_payload():
    return {
        "name": "Test System",
        "purpose": "A test system",
        "data_types": ["personal", "financial"],
        "decision_making_role": "automated",
        "status": "active",
        "version": "1.0.0",
        "lifecycle_status": "in_production",
        "owner": "test_owner",
        "department": "Engineering",
        "business_capability": "Customer Service",
        "internal_external_users": "internal",
        "criticality": "high",
        "implementation_stage": "deployed",
        "ai_type": "generative",
        "vendor": "Test Vendor",
        "model_name": "Test Model",
        "model_version": "v2",
        "api_provider": "OpenAI",
        "framework": "LangChain",
        "hosting": "AWS",
        "integrations": ["slack"],
        "authentication_method": "oauth2",
        "vector_db": "Pinecone",
        "knowledge_sources": ["wiki"],
        "workflow_engine": "Airflow",
        "agent_framework": "AutoGPT",
        "deployment_type": "cloud",
        "data_flow": "sync",
        "apis": ["api1"],
        "databases": ["db1"],
        "event_systems": "kafka",
        "caching": "redis",
        "monitoring": "datadog",
        "logging": "splunk",
        "deployment_details": "k8s",
        "data_sensitivity": "confidential",
        "data_sources": ["db1"],
        "data_destinations": ["s3"],
        "usage_frequency": "daily",
        "users_count": 100,
        "uptime": 99.9,
        "approvals_required": True,
        "risk_classification": "low",
        "oversight_status": "approved",
        "documentation_status": "complete",
        "applicable_policies": ["policy1"],
        "rbac_enabled": True,
        "encryption_status": "encrypted",
        "incident_count": 0,
        "applicable_regulations": ["GDPR"],
        "obligations": ["logging"],
        "evidence_status": "collected",
        "cost": 1000.50,
        "roi_notes": "positive",
        "licensing_type": "commercial",
        "planned_changes": "none",
        "roadmap_notes": "Q4 update",
        "data_quality_notes": "Good data",
        "data_owner": "Data Team",
        "data_freshness": "daily",
        "data_accessibility": ["internal_system"],
        "data_availability": "highly available"
    }

@pytest.fixture
def chatbot_payload():
    return {
        "name": "Customer Support Chatbot",
        "purpose": "First-line customer support",
        "data_types": ["customer_messages", "account_info"],
        "decision_making_role": "informational",
        "status": "active",
        "version": "2.1.0",
        "lifecycle_status": "in_production",
        "owner": "support_team",
        "department": "Customer Success",
        "business_capability": "Support",
        "internal_external_users": "external",
        "criticality": "medium",
        "implementation_stage": "deployed",
        "ai_type": "generative",
        "vendor": "OpenAI",
        "model_name": "GPT-4",
        "model_version": "0613",
        "api_provider": "Azure",
        "framework": "LangChain",
        "hosting": "Azure",
        "integrations": ["zendesk", "slack"],
        "authentication_method": "api_key",
        "vector_db": "Pinecone",
        "knowledge_sources": ["help_center", "kb"],
        "workflow_engine": "none",
        "agent_framework": "custom",
        "deployment_type": "cloud",
        "data_flow": "sync",
        "apis": ["zendesk_api"],
        "databases": ["postgres"],
        "event_systems": "none",
        "caching": "redis",
        "monitoring": "datadog",
        "logging": "azure_monitor",
        "deployment_details": "kubernetes",
        "data_sensitivity": "confidential",
        "data_sources": ["zendesk"],
        "data_destinations": ["zendesk"],
        "usage_frequency": "continuous",
        "users_count": 50000,
        "uptime": 99.5,
        "approvals_required": False,
        "risk_classification": "low",
        "oversight_status": "reviewed",
        "documentation_status": "complete",
        "applicable_policies": ["acceptable_use", "privacy_policy"],
        "rbac_enabled": True,
        "encryption_status": "encrypted",
        "incident_count": 2,
        "applicable_regulations": ["GDPR", "CCPA"],
        "obligations": ["data_deletion", "opt_out"],
        "evidence_status": "collected",
        "cost": 5000.0,
        "roi_notes": "Reduces ticket load by 30%",
        "licensing_type": "api",
        "planned_changes": "upgrade to new model",
        "roadmap_notes": "Q3 2024"
    }

@pytest.fixture
def hiring_screener_payload():
    return {
        "name": "Resume Screener",
        "purpose": "Automated resume filtering",
        "data_types": ["resumes", "demographics"],
        "decision_making_role": "automated_filtering",
        "status": "active",
        "version": "1.0",
        "lifecycle_status": "in_production",
        "owner": "hr_team",
        "department": "Human Resources",
        "business_capability": "Recruiting",
        "internal_external_users": "internal",
        "criticality": "high",
        "implementation_stage": "deployed",
        "ai_type": "predictive",
        "vendor": "AcmeHR",
        "model_name": "Screener",
        "model_version": "v1",
        "api_provider": "AcmeHR",
        "framework": "custom",
        "hosting": "SaaS",
        "integrations": ["workday"],
        "authentication_method": "oauth2",
        "vector_db": "none",
        "knowledge_sources": ["job_descriptions"],
        "workflow_engine": "none",
        "agent_framework": "none",
        "deployment_type": "saas",
        "data_flow": "batch",
        "apis": ["workday_api"],
        "databases": ["snowflake"],
        "event_systems": "none",
        "caching": "none",
        "monitoring": "vendor_dashboard",
        "logging": "vendor_dashboard",
        "deployment_details": "managed_by_vendor",
        "data_sensitivity": "highly_confidential",
        "data_sources": ["workday"],
        "data_destinations": ["workday"],
        "usage_frequency": "daily",
        "users_count": 20,
        "uptime": 99.9,
        "approvals_required": True,
        "risk_classification": "high",
        "oversight_status": "under_review",
        "documentation_status": "in_progress",
        "applicable_policies": ["anti_discrimination", "hiring_policy"],
        "rbac_enabled": True,
        "encryption_status": "encrypted",
        "incident_count": 0,
        "applicable_regulations": ["GDPR", "EEOC"],
        "obligations": ["fairness_audit", "explainability"],
        "evidence_status": "missing",
        "cost": 12000.0,
        "roi_notes": "Saves 40 hours/week",
        "licensing_type": "subscription",
        "planned_changes": "none",
        "roadmap_notes": "Evaluate alternative vendors"
    }

@pytest.fixture
def healthcare_diagnostic_payload():
    return {
        "name": "Medical Imaging Diagnostic",
        "purpose": "Assists radiologists in finding anomalies",
        "data_types": ["medical_images", "patient_health_data"],
        "decision_making_role": "human_in_the_loop",
        "status": "active",
        "version": "3.2.1",
        "lifecycle_status": "in_production",
        "owner": "clinical_ops",
        "department": "Radiology",
        "business_capability": "Diagnostics",
        "internal_external_users": "internal",
        "criticality": "critical",
        "implementation_stage": "deployed",
        "ai_type": "computer_vision",
        "vendor": "HealthAI",
        "model_name": "VisionDiag",
        "model_version": "2023.1",
        "api_provider": "none",
        "framework": "TensorFlow",
        "hosting": "on_premise",
        "integrations": ["epic_emr"],
        "authentication_method": "mtls",
        "vector_db": "none",
        "knowledge_sources": ["training_dataset_v3"],
        "workflow_engine": "custom",
        "agent_framework": "none",
        "deployment_type": "on_premise",
        "data_flow": "sync",
        "apis": ["dicom_api"],
        "databases": ["pacs"],
        "event_systems": "hl7",
        "caching": "none",
        "monitoring": "custom",
        "logging": "splunk",
        "deployment_details": "bare_metal",
        "data_sensitivity": "phi",
        "data_sources": ["pacs"],
        "data_destinations": ["epic_emr"],
        "usage_frequency": "continuous",
        "users_count": 50,
        "uptime": 99.99,
        "approvals_required": True,
        "risk_classification": "unacceptable",
        "oversight_status": "approved",
        "documentation_status": "complete",
        "applicable_policies": ["phi_handling", "medical_device_policy"],
        "rbac_enabled": True,
        "encryption_status": "encrypted",
        "incident_count": 0,
        "applicable_regulations": ["HIPAA", "FDA"],
        "obligations": ["audit_trail", "accuracy_reporting"],
        "evidence_status": "collected",
        "cost": 150000.0,
        "roi_notes": "Improves detection rate by 15%",
        "licensing_type": "perpetual",
        "planned_changes": "hardware upgrade",
        "roadmap_notes": "expand to mri"
    }

@pytest.fixture
def credit_scoring_payload():
    return {
        "name": "Credit Risk Scorer",
        "purpose": "Calculates credit scores for loan applicants",
        "data_types": ["financial_history", "demographics"],
        "decision_making_role": "automated_decision",
        "status": "active",
        "version": "5.0",
        "lifecycle_status": "in_production",
        "owner": "risk_team",
        "department": "Risk Management",
        "business_capability": "Underwriting",
        "internal_external_users": "internal",
        "criticality": "critical",
        "implementation_stage": "deployed",
        "ai_type": "machine_learning",
        "vendor": "Internal",
        "model_name": "XGBoostScorer",
        "model_version": "v5",
        "api_provider": "Internal",
        "framework": "scikit-learn",
        "hosting": "AWS",
        "integrations": ["loan_origination_system"],
        "authentication_method": "iam",
        "vector_db": "none",
        "knowledge_sources": ["historical_loans"],
        "workflow_engine": "step_functions",
        "agent_framework": "none",
        "deployment_type": "cloud",
        "data_flow": "sync",
        "apis": ["internal_scoring_api"],
        "databases": ["aurora"],
        "event_systems": "eventbridge",
        "caching": "none",
        "monitoring": "datadog",
        "logging": "cloudwatch",
        "deployment_details": "sagemaker",
        "data_sensitivity": "highly_confidential",
        "data_sources": ["experian_api"],
        "data_destinations": ["loan_origination_system"],
        "usage_frequency": "continuous",
        "users_count": 100,
        "uptime": 99.95,
        "approvals_required": True,
        "risk_classification": "high",
        "oversight_status": "approved",
        "documentation_status": "complete",
        "applicable_policies": ["fair_lending", "model_risk_management"],
        "rbac_enabled": True,
        "encryption_status": "encrypted",
        "incident_count": 1,
        "applicable_regulations": ["FCRA", "ECOA"],
        "obligations": ["adverse_action_notices", "bias_testing"],
        "evidence_status": "collected",
        "cost": 50000.0,
        "roi_notes": "Reduces default rate",
        "licensing_type": "internal",
        "planned_changes": "retrain model in Q4",
        "roadmap_notes": "include alternative data sources"
    }

@pytest.fixture
def internal_copilot_payload():
    return {
        "name": "Developer Copilot",
        "purpose": "Code completion and generation",
        "data_types": ["source_code", "documentation"],
        "decision_making_role": "informational",
        "status": "active",
        "version": "1.0",
        "lifecycle_status": "in_production",
        "owner": "platform_engineering",
        "department": "Engineering",
        "business_capability": "Development",
        "internal_external_users": "internal",
        "criticality": "low",
        "implementation_stage": "deployed",
        "ai_type": "generative",
        "vendor": "GitHub",
        "model_name": "Copilot",
        "model_version": "latest",
        "api_provider": "GitHub",
        "framework": "none",
        "hosting": "SaaS",
        "integrations": ["vscode", "intellij"],
        "authentication_method": "sso",
        "vector_db": "none",
        "knowledge_sources": ["public_code"],
        "workflow_engine": "none",
        "agent_framework": "none",
        "deployment_type": "saas",
        "data_flow": "sync",
        "apis": ["github_api"],
        "databases": ["none"],
        "event_systems": "none",
        "caching": "none",
        "monitoring": "vendor",
        "logging": "vendor",
        "deployment_details": "ide_plugin",
        "data_sensitivity": "confidential",
        "data_sources": ["local_ide"],
        "data_destinations": ["github"],
        "usage_frequency": "continuous",
        "users_count": 200,
        "uptime": 99.0,
        "approvals_required": False,
        "risk_classification": "low",
        "oversight_status": "approved",
        "documentation_status": "complete",
        "applicable_policies": ["acceptable_use"],
        "rbac_enabled": True,
        "encryption_status": "encrypted",
        "incident_count": 0,
        "applicable_regulations": ["none"],
        "obligations": ["license_compliance"],
        "evidence_status": "not_required",
        "cost": 40000.0,
        "roi_notes": "15% increase in developer productivity",
        "licensing_type": "subscription",
        "planned_changes": "none",
        "roadmap_notes": "roll out to QA team"
    }

def get_auth_headers(user):
    from dependencies import oauth2_scheme
    from jose import jwt
    from config import settings

    # generate a valid JWT token
    to_encode = {"sub": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"Authorization": f"Bearer {encoded_jwt}"}

@pytest.mark.asyncio
@pytest.mark.parametrize("payload_name", ["system_payload", "chatbot_payload", "credit_scoring_payload"])
async def test_create_ai_system(db_session: AsyncSession, user, request, payload_name):
    headers = get_auth_headers(user)
    # If the fixture is async, await it, otherwise get its value
    fixture_value = request.getfixturevalue(payload_name)
    if hasattr(fixture_value, "__await__"):
        payload = await fixture_value
    else:
        payload = fixture_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/ai-systems", json=payload, headers=headers)

        assert response.status_code == 201
        data = response.json()

        # Test original fields
        assert data["name"] == payload["name"]
        assert data["purpose"] == payload["purpose"]
        assert data["data_types"] == payload["data_types"]
        assert data["decision_making_role"] == payload["decision_making_role"]
        assert data["status"] == payload["status"]
        assert "id" in data
        assert "organization_id" in data

        # Test new fields round-trip correctly
        for key, value in payload.items():
            assert data.get(key) == value, f"Mismatch for field {key}: expected {value}, got {data.get(key)}"

@pytest.mark.asyncio
async def test_list_ai_systems(db_session: AsyncSession, user, organization: Organization, system_payload):
    headers = get_auth_headers(user)

    # Create system first
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/api/ai-systems", json=system_payload, headers=headers)

        response = await client.get("/api/ai-systems", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["name"] == system_payload["name"]

@pytest.mark.asyncio
async def test_get_ai_system(db_session: AsyncSession, user, organization: Organization, system_payload):
    headers = get_auth_headers(user)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/ai-systems", json=system_payload, headers=headers)
        system_id = create_res.json()["id"]

        get_res = await client.get(f"/api/ai-systems/{system_id}", headers=headers)
        assert get_res.status_code == 200
        assert get_res.json()["id"] == system_id

@pytest.mark.asyncio
@pytest.mark.parametrize("payload_name", ["system_payload", "chatbot_payload", "credit_scoring_payload"])
async def test_update_ai_system(db_session: AsyncSession, user, organization: Organization, request, payload_name):
    headers = get_auth_headers(user)
    fixture_value = request.getfixturevalue(payload_name)
    if hasattr(fixture_value, "__await__"):
        payload = await fixture_value
    else:
        payload = fixture_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/ai-systems", json=payload, headers=headers)
        system_id = create_res.json()["id"]

        update_payload = {"name": "Updated System"}
        # also update a few other fields to test
        if "vendor" in payload:
            update_payload["vendor"] = "Updated Vendor"
        if "incident_count" in payload:
            update_payload["incident_count"] = 5

        update_res = await client.put(f"/api/ai-systems/{system_id}", json=update_payload, headers=headers)
        assert update_res.status_code == 200
        data = update_res.json()
        assert data["name"] == "Updated System"
        assert data["status"] == payload["status"]
        if "vendor" in payload:
            assert data["vendor"] == "Updated Vendor"
        if "incident_count" in payload:
            assert data["incident_count"] == 5

        # Verify other fields remain unchanged
        for key, value in payload.items():
            if key not in update_payload:
                assert data.get(key) == value, f"Mismatch for field {key} after update"

@pytest.mark.asyncio
async def test_delete_ai_system(db_session: AsyncSession, user, organization: Organization, system_payload):
    headers = get_auth_headers(user)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        create_res = await client.post("/api/ai-systems", json=system_payload, headers=headers)
        system_id = create_res.json()["id"]

        delete_res = await client.delete(f"/api/ai-systems/{system_id}", headers=headers)
        assert delete_res.status_code == 200

        get_res = await client.get(f"/api/ai-systems/{system_id}", headers=headers)
        assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_ai_system_technology_fields(db_session: AsyncSession, organization: Organization):
    """
    Test that the new technology fields map correctly in SQLAlchemy,
    defaults are applied properly, and types behave as expected.
    """
    sys = AISystem(
        organization_id=organization.id,
        name="Tech Test System",
        vendor="OpenAI",
        model_name="GPT-4",
        model_version="0613",
        api_provider="Azure",
        framework="LangChain",
        hosting="Cloud",
        authentication_method="OAuth2",
        vector_db="Pinecone",
        workflow_engine="Airflow",
        agent_framework="AutoGPT"
    )
    db_session.add(sys)
    await db_session.commit()
    await db_session.refresh(sys)

    assert sys.vendor == "OpenAI"
    assert sys.model_name == "GPT-4"
    assert sys.model_version == "0613"
    assert sys.api_provider == "Azure"
    assert sys.framework == "LangChain"
    assert sys.hosting == "Cloud"
    assert sys.authentication_method == "OAuth2"
    assert sys.vector_db == "Pinecone"
    assert sys.workflow_engine == "Airflow"
    assert sys.agent_framework == "AutoGPT"

    # Test JSONB default properties
    assert sys.integrations == []
    assert sys.knowledge_sources == []

    # Update JSONB fields and test persistence
    sys.integrations = ["Jira", "Slack"]
    sys.knowledge_sources = ["Confluence", "Google Drive"]
    await db_session.commit()
    await db_session.refresh(sys)

    assert sys.integrations == ["Jira", "Slack"]
    assert sys.knowledge_sources == ["Confluence", "Google Drive"]


@pytest.mark.asyncio
async def test_create_ai_system_with_extended_fields(db_session: AsyncSession, user, system_payload):
    headers = get_auth_headers(user)

    # Extend the payload with new optional fields
    extended_payload = system_payload.copy()
    extended_payload.update({
        "vendor": "Acme AI Corp",
        "risk_classification": "High Risk",
        "users_count": 500,
        "incident_count": 2,
        "knowledge_sources": ["wiki", "internal docs"]
    })

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/ai-systems", json=extended_payload, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["vendor"] == "Acme AI Corp"
        assert data["risk_classification"] == "High Risk"
        assert data["users_count"] == 500
        assert data["incident_count"] == 2
        assert data["knowledge_sources"] == ["wiki", "internal docs"]

        # Original fields should still match
        assert data["name"] == system_payload["name"]
        assert data["purpose"] == system_payload["purpose"]

@pytest.mark.asyncio
async def test_ai_system_ownership_isolation(db_session: AsyncSession, user, user2, system_payload):
    headers1 = get_auth_headers(user)
    headers2 = get_auth_headers(user2)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # User 1 creates system
        create_res = await client.post("/api/ai-systems", json=system_payload, headers=headers1)
        system_id = create_res.json()["id"]

        # User 2 tries to access it
        get_res = await client.get(f"/api/ai-systems/{system_id}", headers=headers2)
        assert get_res.status_code == 404

        # User 2 tries to update it
        update_res = await client.put(f"/api/ai-systems/{system_id}", json={"name": "hacked"}, headers=headers2)
        assert update_res.status_code == 404

        # User 2 tries to delete it
        delete_res = await client.delete(f"/api/ai-systems/{system_id}", headers=headers2)
        assert delete_res.status_code == 404

@pytest.mark.asyncio
async def test_ai_system_reproducibility(db_session: AsyncSession, user, healthcare_diagnostic_payload):
    headers = get_auth_headers(user)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create first system
        res1 = await client.post("/api/ai-systems", json=healthcare_diagnostic_payload, headers=headers)
        assert res1.status_code == 201
        data1 = res1.json()

        # Create second system with identical payload
        res2 = await client.post("/api/ai-systems", json=healthcare_diagnostic_payload, headers=headers)
        assert res2.status_code == 201
        data2 = res2.json()

        # Remove generated fields
        generated_fields = {"id", "organization_id", "created_at", "updated_at"}
        for field in generated_fields:
            data1.pop(field, None)
            data2.pop(field, None)

        # Assert all remaining fields are identical
        assert data1 == data2

from models.adoption_record import AdoptionRecord
import uuid
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_capability_map_missing_scores(db_session, user, organization):
    sys_id = uuid.uuid4()
    sys_empty = AISystem(
        id=sys_id,
        organization_id=organization.id,
        name="Empty Score System",
        ai_type="predictive",
        criticality="low",
        lifecycle_status="development"
    )
    db_session.add(sys_empty)
    await db_session.commit()

    headers = get_auth_headers(user)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/ai-systems/capability-map", headers=headers)

    assert response.status_code == 200
    data = response.json()
    sys_data = next((s for s in data if s["id"] == str(sys_id)), None)
    assert sys_data is not None

    assert sys_data["name"] == "Empty Score System"
    assert sys_data["adoption_score"] is None
    assert sys_data["data_score"] is None
    assert sys_data["roi_score"] is None
    assert sys_data["cost_is_partial"] is True

@pytest.mark.asyncio
async def test_capability_map_populated_scores(db_session, user, organization):
    sys_id = uuid.uuid4()
    sys_populated = AISystem(
        id=sys_id,
        organization_id=organization.id,
        name="Populated Score System",
        ai_type="generative",
        criticality="high",
        lifecycle_status="deployed",
        data_types=["text", "images"],
        data_sources=["crm", "public"],
        data_destinations=["internal_db"],
        expected_benefits=50000.0,
        cloud_cost=1000.0,
        licensing_cost=500.0,
        maintenance_cost=200.0,
        inference_cost=300.0,
        cost_currency="USD"
    )
    db_session.add(sys_populated)
    await db_session.flush()

    ar = AdoptionRecord(
        id=uuid.uuid4(),
        ai_system_id=sys_id,
        department="Engineering",
        organization_id=organization.id,
        user_count=100,
        training_status="completed",
    )
    db_session.add(ar)
    await db_session.commit()

    headers = get_auth_headers(user)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/ai-systems/capability-map", headers=headers)

    assert response.status_code == 200
    data = response.json()
    sys_data = next((s for s in data if s["id"] == str(sys_id)), None)
    assert sys_data is not None

    assert sys_data["name"] == "Populated Score System"
    assert sys_data["adoption_score"] == 95.0
    assert sys_data["data_score"] is not None
    assert sys_data["roi_score"] is None
    assert sys_data["cost_is_partial"] is False
    assert len(sys_data["cost_missing_components"]) == 0
    assert "text" in sys_data["data_types"]
