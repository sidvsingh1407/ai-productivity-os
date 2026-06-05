import pytest
from backend.workflows.workflow_intelligence_engine import generate_workflow_intelligence

def test_generate_workflow_intelligence_manual_approval():
    input_config = {
        "workflowDescription": "I send an email to my manager for approval.",
        "currentChallenges": "Approval is delayed often.",
        "currentToolsUsed": "email",
        "teamSize": "5",
        "department": "HR"
    }
    result = generate_workflow_intelligence(input_config)
    assert result["executive_summary"]["workflow_risk_level"] == "High"

    bottleneck_titles = [b["title"] for b in result["bottlenecks"]]
    assert "Manual Approval Dependencies" in bottleneck_titles

def test_generate_workflow_intelligence_fragmentation():
    input_config = {
        "workflowDescription": "I manually copy data from excel to a spreadsheet.",
        "currentChallenges": "It's annoying to re-key data.",
        "currentToolsUsed": "excel, spreadsheet, text editor, word, powerpoint",
        "teamSize": "2",
        "department": "Finance"
    }
    result = generate_workflow_intelligence(input_config)

    bottleneck_titles = [b["title"] for b in result["bottlenecks"]]
    assert "Operational Fragmentation" in bottleneck_titles
