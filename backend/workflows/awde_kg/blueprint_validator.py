from __future__ import annotations

from copy import deepcopy
from typing import Any

from .config import AUTOMATION_TIERS


def validate_blueprint_json(blueprint_json: dict[str, Any]) -> dict[str, Any]:
    original = deepcopy(blueprint_json)
    corrected = normalize_blueprint(blueprint_json)
    errors = collect_errors(original, corrected)
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "corrected_blueprint": original if not errors else corrected,
    }


def normalize_blueprint(blueprint_json: dict[str, Any]) -> dict[str, Any]:
    blueprint = deepcopy(blueprint_json)
    blueprint.setdefault("title", "Automation Blueprint")
    if blueprint.get("automation_tier") not in AUTOMATION_TIERS:
        blueprint["automation_tier"] = "hitl" if blueprint.get("hitl_checkpoint") else "augmented"
    blueprint["orchestration_pipeline"] = normalize_pipeline(blueprint.get("orchestration_pipeline"))
    blueprint["hitl_checkpoint"] = normalize_hitl_checkpoint(
        blueprint.get("hitl_checkpoint"),
        blueprint["orchestration_pipeline"],
        blueprint["automation_tier"],
    )
    blueprint.setdefault("estimated_time_saved", "6-12 hours/month")
    blueprint["confidence"] = normalize_confidence(blueprint.get("confidence"))
    return blueprint


def normalize_pipeline(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        value = [
            {
                "step": 1,
                "action": "analyze_work_item",
                "capability_id": "capability:decision_support",
                "input": "workflow_step_payload",
                "output": "validated_decision_payload",
                "hitl_required": True,
            }
        ]
    normalized = []
    previous_output = None
    for index, raw_step in enumerate(value[:5], start=1):
        step = raw_step if isinstance(raw_step, dict) else {}
        action = clean_text(step.get("action"), f"execute_step_{index}")
        capability_id = clean_capability_id(step.get("capability_id"))
        step_input = clean_text(step.get("input"), previous_output or "workflow_step_payload")
        step_output = clean_text(step.get("output"), output_for_action(action))
        normalized_step = {
            "step": index,
            "action": action,
            "capability_id": capability_id,
            "input": step_input,
            "output": step_output,
            "hitl_required": bool(step.get("hitl_required", False)),
        }
        normalized.append(normalized_step)
        previous_output = step_output
    return normalized


def normalize_hitl_checkpoint(value: Any, pipeline: list[dict[str, Any]], automation_tier: str) -> str | None:
    hitl_steps = [step for step in pipeline if step["hitl_required"]]
    if automation_tier == "hitl" and not hitl_steps:
        pipeline[min(1, len(pipeline) - 1)]["hitl_required"] = True
        hitl_steps = [step for step in pipeline if step["hitl_required"]]
    if hitl_steps and not isinstance(value, str):
        return "Pause at the HITL-marked step for human validation before downstream execution."
    if not hitl_steps:
        return None
    return clean_text(value, "Pause for human validation before downstream execution.")


def normalize_confidence(value: Any) -> float:
    if not isinstance(value, (float, int)):
        return 0.65
    return round(max(0.0, min(1.0, float(value))), 4)


def collect_errors(original: dict[str, Any], corrected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"title", "automation_tier", "orchestration_pipeline", "hitl_checkpoint", "estimated_time_saved", "confidence"}
    missing = sorted(field for field in required if field not in original)
    if missing:
        errors.append(f"missing required fields: {missing}")
    if original.get("automation_tier") not in AUTOMATION_TIERS:
        errors.append("automation_tier must be full, hitl, or augmented")
    pipeline = original.get("orchestration_pipeline")
    if not isinstance(pipeline, list) or not pipeline:
        errors.append("orchestration_pipeline must be a non-empty list")
    elif len(pipeline) > 5:
        errors.append("orchestration_pipeline must have at most 5 steps")
    if isinstance(pipeline, list):
        for index, step in enumerate(pipeline[:5], start=1):
            if not isinstance(step, dict):
                errors.append(f"step {index} must be an object")
                continue
            step_errors = step_errors_for(index, step)
            errors.extend(step_errors)
    confidence = original.get("confidence")
    if not isinstance(confidence, (float, int)) or not 0.0 <= float(confidence) <= 1.0:
        errors.append("confidence must be a float from 0.0 to 1.0")
    hitl_steps = corrected["orchestration_pipeline"]
    has_hitl_step = any(step["hitl_required"] for step in hitl_steps)
    if has_hitl_step and not isinstance(original.get("hitl_checkpoint"), str):
        errors.append("hitl_checkpoint must be a string when any step requires HITL")
    if not has_hitl_step and original.get("hitl_checkpoint") is not None:
        errors.append("hitl_checkpoint must be null when no step requires HITL")
    if corrected != original:
        errors.append("blueprint required correction for schema, HITL, or orchestration consistency")
    return unique(errors)


def step_errors_for(index: int, step: dict[str, Any]) -> list[str]:
    errors = []
    required = {"step", "action", "capability_id", "input", "output", "hitl_required"}
    missing = sorted(field for field in required if field not in step)
    if missing:
        errors.append(f"step {index} missing required fields: {missing}")
    if step.get("step") != index:
        errors.append(f"step {index} must have step={index}")
    if not isinstance(step.get("action"), str) or not step.get("action"):
        errors.append(f"step {index} action must be a non-empty string")
    if not isinstance(step.get("capability_id"), str) or not str(step.get("capability_id")).startswith("capability:"):
        errors.append(f"step {index} capability_id must start with capability:")
    if not isinstance(step.get("input"), str) or not step.get("input"):
        errors.append(f"step {index} input must be a non-empty string")
    if not isinstance(step.get("output"), str) or not step.get("output"):
        errors.append(f"step {index} output must be a non-empty string")
    if not isinstance(step.get("hitl_required"), bool):
        errors.append(f"step {index} hitl_required must be boolean")
    return errors


def clean_text(value: Any, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def clean_capability_id(value: Any) -> str:
    if isinstance(value, str) and value.startswith("capability:"):
        return value
    return "capability:decision_support"


def output_for_action(action: str) -> str:
    if "extract" in action:
        return "structured_fields"
    if "classify" in action:
        return "classification_label_and_route"
    if "resolve" in action or "match" in action:
        return "matched_entity_payload"
    if "validate" in action:
        return "validated_decision_payload"
    return "workflow_step_output"


def unique(values: list[str]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output
