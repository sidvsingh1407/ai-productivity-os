from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from fastapi import HTTPException, status

from . import repository
from .pipeline import run_pipeline
from typing import List, Optional
from .schemas import WorkflowDetailResponse, WorkflowResponse, BlueprintResponse, WorkflowIntelligence
from .workflow_intelligence_engine import generate_workflow_intelligence
from .diagnostic_engine import calculate_diagnostic_scores
from services.narrative_service import generate_workflow_narrative

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
        else:
            # Legacy intelligence path (old)
            intelligence_payload = generate_workflow_intelligence(input_config)

            # 3.5 Generate dynamic narrative
            workflow_context = {
                "company_name": input_config.get("companyName", "the organization"),
                "industry": input_config.get("industry", "unspecified"),
                "company_size": input_config.get("companySize", "unspecified"),
                "workflow_description": input_config.get("workflowDescription", "unspecified"),
                "automation_level": input_config.get("currentAutomationLevel", "unspecified")
            }

            narrative_scores = {
                "workflow_maturity": intelligence_payload.get("workflow_maturity", "unspecified"),
                "automation_score": intelligence_payload.get("automation_coverage", "unspecified"),
                "friction_score": "unspecified", # Derived/not currently output by engine explicitly
                "ai_opportunity_score": "unspecified" # Derived/not currently output by engine explicitly
            }

            narrative = await generate_workflow_narrative(narrative_scores, workflow_context)

            narrative_source = "static"
            if narrative:
                narrative_source = "dynamic"
                if "executive_summary" in narrative:
                    for key in ["most_critical_bottleneck", "primary_root_cause", "highest_priority_intervention", "workflow_risk_level", "workflow_maturity"]:
                        if key in narrative["executive_summary"]:
                            intelligence_payload["executive_summary"][key] = narrative["executive_summary"][key]

                    # Also copy the top level fields in intelligence payload
                    intelligence_payload["most_critical_bottleneck"] = intelligence_payload["executive_summary"].get("most_critical_bottleneck", "")
                    intelligence_payload["primary_root_cause"] = intelligence_payload["executive_summary"].get("primary_root_cause", "")
                    intelligence_payload["highest_priority_intervention"] = intelligence_payload["executive_summary"].get("highest_priority_intervention", "")
                    intelligence_payload["workflow_risk_level"] = intelligence_payload["executive_summary"].get("workflow_risk_level", "")
                    intelligence_payload["workflow_maturity"] = intelligence_payload["executive_summary"].get("workflow_maturity", "")

                if "bottlenecks" in narrative and narrative["bottlenecks"]:
                    # Ensure we have root_cause matching the schema
                    new_bottlenecks = []
                    for b in narrative["bottlenecks"]:
                        b["root_cause"] = {
                            "root_cause": intelligence_payload["executive_summary"].get("primary_root_cause", ""),
                            "evidence": "Observed in workflow execution patterns.",
                            "impact": "Reduces operational throughput."
                        }
                        new_bottlenecks.append(b)
                    intelligence_payload["bottlenecks"] = new_bottlenecks

                if "automation_opportunities" in narrative and narrative["automation_opportunities"]:
                    # While the prompt generates this, WorkflowIntelligence doesn't natively map it directly to
                    # a top-level field that mirrors this unless it maps to recommendations or blueprints.
                    pass # Extracted but not mapped in original intelligence, schema does not have it

                if "recommendations" in narrative and narrative["recommendations"]:
                    intelligence_payload["recommendations"] = narrative["recommendations"]

            intelligence = WorkflowIntelligence(**intelligence_payload)

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
