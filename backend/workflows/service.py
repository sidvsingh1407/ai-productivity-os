from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from fastapi import HTTPException, status

from . import repository
from .pipeline import run_pipeline
from typing import List, Optional
from .schemas import WorkflowDetailResponse, WorkflowResponse, BlueprintResponse
from .diagnostic_engine import calculate_diagnostic_scores

import uuid

async def run_workflow(db: AsyncSession, org_id: uuid.UUID, user_id: uuid.UUID, input_config: Dict[str, Any], steps_input: Optional[List[Dict[str, Any]]] = None) -> WorkflowDetailResponse:
    # 1. create workflow record (status: running)
    workflow = await repository.create_workflow(db, org_id, user_id, input_config, steps_input=steps_input)

    try:
        # 2. call pipeline.run_pipeline(input_config)
        # Note: in a real production scenario this might be pushed to Celery.
        # Running synchronously here as per the architecture spec for now.
        result = run_pipeline(input_config)

        # 3. save blueprints to DB
        blueprints = await repository.save_blueprints(db, workflow.id, result.get("blueprints", []))

        # Update workflow status to complete
        workflow = await repository.update_workflow_status(db, workflow, "complete")

        intelligence = None
        narrative_source = None

        if steps_input is not None:
            # Deterministic engine path (new)
            diagnostic_results = calculate_diagnostic_scores(steps_input)
            workflow = await repository.update_workflow_diagnostics(
                db,
                workflow,
                diagnostic_results["scores"],
                diagnostic_results["findings"]
            )

        # 4. return WorkflowDetailResponse
        workflow_resp = WorkflowResponse.model_validate(workflow)
        blueprint_resps = [BlueprintResponse.model_validate(bp) for bp in blueprints]

        return WorkflowDetailResponse(
            **workflow_resp.model_dump(),
            blueprints=blueprint_resps,
            intelligence=intelligence,
            narrative_source=narrative_source
        )

    except Exception as e:
        await repository.update_workflow_status(db, workflow, "failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow execution failed: {str(e)}"
        )
