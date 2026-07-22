import pytest
from workflows.diagnostic_engine import calculate_diagnostic_scores

@pytest.fixture
def well_governed_steps():
    return [
        {"step_name": "Step 1", "owner_role": "Analyst", "requires_approval": False, "system_tool": "Jira", "manual_handoff": False},
        {"step_name": "Step 2", "owner_role": "Manager", "requires_approval": True, "system_tool": "Jira", "manual_handoff": False},
        {"step_name": "Step 3", "owner_role": "Director", "requires_approval": True, "system_tool": "Workday", "manual_handoff": False}
    ]

@pytest.fixture
def bottlenecked_steps():
    return [
        {"step_name": "Step 1", "owner_role": "Analyst", "requires_approval": False, "system_tool": "Jira", "manual_handoff": False},
        {"step_name": "Step 2", "owner_role": "Analyst", "requires_approval": False, "system_tool": None, "manual_handoff": True},
        {"step_name": "Step 3", "owner_role": "Manager", "requires_approval": True, "system_tool": None, "manual_handoff": True}
    ]

@pytest.fixture
def ambiguous_steps():
    return [
        {"step_name": "Step 1", "owner_role": None, "requires_approval": False, "system_tool": None, "manual_handoff": False},
        {"step_name": "Step 2", "owner_role": "Analyst", "requires_approval": False, "system_tool": None, "manual_handoff": False},
        {"step_name": "Step 3", "owner_role": None, "requires_approval": False, "system_tool": "Jira", "manual_handoff": False}
    ]

def test_well_governed_workflow(well_governed_steps):
    results = calculate_diagnostic_scores(well_governed_steps)
    scores = results["scores"]

    assert scores["bottleneck"] == 100
    assert scores["governance"] == 100
    assert scores["ambiguity"] == 100
    assert scores["risk"] == 100

    findings = results["findings"]
    assert any("High governance" in strength for strength in findings["strengths"])

def test_bottlenecked_workflow(bottlenecked_steps):
    results = calculate_diagnostic_scores(bottlenecked_steps)
    scores = results["scores"]

    # manual_handoff count = 2. missing tool (non-manual) = 0.
    # total steps = 3.
    # Penalty: (2/3) * 50 = 33. Score = 66
    assert scores["bottleneck"] == 66
    assert scores["ambiguity"] == 33

    findings = results["findings"]
    assert len(findings["priority_actions"]) > 0

def test_ambiguous_workflow(ambiguous_steps):
    results = calculate_diagnostic_scores(ambiguous_steps)
    scores = results["scores"]

    # 0 steps have both owner AND tool. total = 3.
    # Score = 0
    assert scores["ambiguity"] == 0

    # missing owner on 2 steps. total = 3. Penalty = (2/3)*40 = 26.666...
    # missing system_tool on approval? No approvals here.
    assert scores["governance"] == 73 # int(100 - 26.666)

    findings = results["findings"]
    assert any("ambiguous" in weakness for weakness in findings["weaknesses"])
