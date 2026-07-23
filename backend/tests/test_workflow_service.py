import pytest
from unittest.mock import patch, MagicMock
from workflows.service import run_workflow
import uuid

@pytest.mark.asyncio
async def test_run_workflow_with_steps_input():
    # Verify that the diagnostic path is taken when steps_input is provided
    org_id = uuid.uuid4()
    user_id = uuid.uuid4()

    mock_db = MagicMock()

    mock_workflow = MagicMock()
    mock_workflow.id = uuid.uuid4()
    mock_workflow.org_id = org_id
    mock_workflow.user_id = user_id
    mock_workflow.status = "complete"
    mock_workflow.input_config = {}
    mock_workflow.steps_input = [
        {"step_name": "Test", "owner_role": "Analyst", "requires_approval": False, "manual_handoff": False, "system_tool": "Jira"}
    ]
    mock_workflow.scores = {"bottleneck": 100, "governance": 100, "ambiguity": 100, "risk": 100, "health": 100}
    mock_workflow.findings = {"strengths": [], "weaknesses": [], "priority_actions": []}
    mock_workflow.created_at = "2023-01-01T00:00:00Z"

    with patch("workflows.repository.create_workflow", return_value=mock_workflow), \
         patch("workflows.pipeline.run_pipeline", return_value={"blueprints": []}), \
         patch("workflows.repository.save_blueprints", return_value=[]), \
         patch("workflows.repository.update_workflow_status", return_value=mock_workflow), \
         patch("workflows.repository.update_workflow_diagnostics", return_value=mock_workflow):

        # Execute run_workflow with steps_input
        result = await run_workflow(mock_db, org_id, user_id, {}, steps_input=mock_workflow.steps_input)

        # Verify result contains the new fields
        assert result.steps_input == mock_workflow.steps_input
        assert result.scores == mock_workflow.scores
        assert result.findings == mock_workflow.findings
        assert result.intelligence is None # Should be skipped
