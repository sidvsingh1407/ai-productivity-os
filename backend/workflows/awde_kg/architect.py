from __future__ import annotations

from .config import AUTOMATION_TIERS


def generate_automation_blueprint(
    process_title: str,
    cognitive_friction: str,
    capability_id: str,
    hitl_need: str,
    confidence: float,
) -> dict[str, dict[str, object]]:
    hitl_required = hitl_need in {"validation", "decision"}
    automation_tier = automation_tier_for(hitl_required, cognitive_friction)
    lead_action = action_for_capability(capability_id)
    pipeline = [
        {
            "step": 1,
            "action": lead_action,
            "capability_id": capability_id,
            "input": input_for_friction(cognitive_friction),
            "output": output_for_capability(capability_id),
            "hitl_required": False,
        },
        {
            "step": 2,
            "action": "validate_decision_payload",
            "capability_id": "capability:decision_support",
            "input": output_for_capability(capability_id),
            "output": "validated_decision_payload",
            "hitl_required": hitl_required,
        },
        {
            "step": 3,
            "action": "execute_or_route_update",
            "capability_id": "capability:orchestration",
            "input": "validated_decision_payload",
            "output": "downstream_workflow_update",
            "hitl_required": False,
        },
    ]
    return {
        "blueprint": {
            "title": f"{process_title.title()} Automation Blueprint",
            "automation_tier": automation_tier,
            "orchestration_pipeline": pipeline,
            "hitl_checkpoint": hitl_checkpoint(hitl_need),
            "estimated_time_saved": estimated_time_saved(cognitive_friction, automation_tier),
            "confidence": round(max(0.0, min(1.0, confidence)), 4),
        }
    }


def automation_tier_for(hitl_required: bool, cognitive_friction: str) -> str:
    if hitl_required:
        return "hitl"
    if cognitive_friction in {"unstructured_data", "routing"}:
        return "full"
    return "augmented"


def action_for_capability(capability_id: str) -> str:
    actions = {
        "capability:document_extraction": "extract_structured_fields",
        "capability:classification": "classify_work_item",
        "capability:summarization": "summarize_work_item",
        "capability:entity_resolution": "resolve_and_match_entities",
        "capability:decision_support": "generate_decision_recommendation",
        "capability:orchestration": "orchestrate_workflow",
    }
    return actions.get(capability_id, "analyze_work_item")


def input_for_friction(cognitive_friction: str) -> str:
    inputs = {
        "unstructured_data": "unstructured_document_or_message",
        "reconciliation": "source_record_and_target_system_record",
        "routing": "incoming_work_item",
        "decision_ambiguity": "case_context_and_policy_constraints",
    }
    return inputs.get(cognitive_friction, "workflow_step_payload")


def output_for_capability(capability_id: str) -> str:
    outputs = {
        "capability:document_extraction": "structured_fields",
        "capability:classification": "classification_label_and_route",
        "capability:summarization": "decision_ready_summary",
        "capability:entity_resolution": "matched_entity_payload",
        "capability:decision_support": "decision_recommendation",
        "capability:orchestration": "workflow_execution_plan",
    }
    return outputs.get(capability_id, "analyzed_payload")


def hitl_checkpoint(hitl_need: str) -> str | None:
    if hitl_need == "decision":
        return "Pause before execution for human approval of the recommended decision and final writeback payload."
    if hitl_need == "validation":
        return "Pause after AI validation so a human can confirm matched fields before downstream update."
    return None


def estimated_time_saved(cognitive_friction: str, automation_tier: str) -> str:
    if automation_tier == "hitl":
        return "8-15 hours/month"
    if cognitive_friction in {"routing", "unstructured_data"}:
        return "10-20 hours/month"
    return "6-12 hours/month"
