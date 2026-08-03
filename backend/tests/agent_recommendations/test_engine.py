from uuid import uuid4
from agent_recommendations.engine import generate_agent_recommendations, normalize_department

def test_normalize_department():
    assert normalize_department("HR") == "hr_agent"
    assert normalize_department("human resources team") == "hr_agent"
    assert normalize_department("SALES") == "sales_agent"
    assert normalize_department("Revenue Ops") == "sales_agent"
    assert normalize_department("legal counsel") == "legal_agent"
    assert normalize_department("finance") == "finance_agent"
    assert normalize_department("tax and accounting") == "finance_agent"
    assert normalize_department("procurement") == "procurement_agent"
    assert normalize_department("supply chain") == "procurement_agent"
    assert normalize_department("Customer Support") == "customer_support_agent"
    assert normalize_department("cx ops") == "customer_support_agent"
    assert normalize_department("IT") is None
    assert normalize_department(None) is None

def test_generate_agent_recommendations_with_department():
    org_id = uuid4()
    opp_id = uuid4()

    opportunities = [
        {
            "id": opp_id,
            "organization_id": org_id,
            "category": "manual_work",
            "title": "Manual HR Tasks",
            "confidence_or_priority": "High",
            "department": "human resources"
        }
    ]

    recs = generate_agent_recommendations(opportunities)
    assert len(recs) == 1
    rec = recs[0]
    assert rec["organization_id"] == org_id
    assert rec["opportunity_id"] == opp_id
    assert rec["agent_type"] == "hr_agent"
    assert rec["confidence"] == "High"
    assert "Recommended hr_agent to address manual_work opportunity (High priority): Manual HR Tasks" in rec["rationale"]

def test_generate_agent_recommendations_knowledge_override():
    opportunities = [
        {
            "id": uuid4(),
            "organization_id": uuid4(),
            "category": "knowledge_bottleneck",
            "title": "Sales Knowledge Issue",
            "confidence_or_priority": "Medium",
            "department": "Sales"
        }
    ]

    recs = generate_agent_recommendations(opportunities)
    assert recs[0]["agent_type"] == "knowledge_agent"

def test_generate_agent_recommendations_customer_override():
    opportunities = [
        {
            "id": uuid4(),
            "organization_id": uuid4(),
            "category": "customer_pain",
            "title": "Finance Customer Issue",
            "confidence_or_priority": "Low",
            "department": "Finance"
        }
    ]

    recs = generate_agent_recommendations(opportunities)
    assert recs[0]["agent_type"] == "customer_support_agent"

def test_generate_agent_recommendations_org_level_or_unrecognized():
    # 1. No department (org level), general category -> executive_agent
    recs = generate_agent_recommendations([{
        "id": uuid4(),
        "organization_id": uuid4(),
        "category": "automation_candidate",
        "title": "Org wide automation",
        "confidence_or_priority": "High",
        "department": None
    }])
    assert recs[0]["agent_type"] == "executive_agent"

    # 2. Unrecognized department (IT), general category -> executive_agent
    recs = generate_agent_recommendations([{
        "id": uuid4(),
        "organization_id": uuid4(),
        "category": "automation_candidate",
        "title": "IT automation",
        "confidence_or_priority": "High",
        "department": "IT Dept"
    }])
    assert recs[0]["agent_type"] == "executive_agent"

    # 3. No department, knowledge category -> knowledge_agent
    recs = generate_agent_recommendations([{
        "id": uuid4(),
        "organization_id": uuid4(),
        "category": "knowledge_bottleneck",
        "title": "Org wide knowledge",
        "confidence_or_priority": "Medium",
        "department": None
    }])
    assert recs[0]["agent_type"] == "knowledge_agent"
