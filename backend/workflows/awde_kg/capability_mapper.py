from __future__ import annotations


ALLOWED_CAPABILITY_TYPES = {
    "document_extraction",
    "classification",
    "summarization",
    "entity_resolution",
    "decision_support",
    "orchestration",
}

AUTOMATION_POTENTIALS = {"low", "medium", "high"}


def map_ai_capability(process_title: str, cognitive_friction: str) -> dict[str, object]:
    process = process_title.lower()
    friction = cognitive_friction.lower()
    capability_type = infer_capability_type(process, friction)
    return {
        "capability_id": f"capability:{capability_type}",
        "capability_type": capability_type,
        "automation_potential": infer_automation_potential(capability_type, friction),
        "reasoning": reasoning(process_title, cognitive_friction, capability_type),
        "confidence": infer_confidence(capability_type, friction),
    }


def infer_capability_type(process: str, friction: str) -> str:
    if friction == "unstructured_data":
        return "document_extraction"
    if friction == "routing":
        return "classification"
    if friction == "reconciliation":
        return "entity_resolution"
    if friction == "decision_ambiguity":
        return "decision_support"
    if any(word in process for word in ["summary", "reporting", "brief"]):
        return "summarization"
    return "orchestration"


def infer_automation_potential(capability_type: str, friction: str) -> str:
    if capability_type in {"document_extraction", "classification", "entity_resolution"}:
        return "high"
    if capability_type in {"decision_support", "summarization"}:
        return "medium"
    if friction == "decision_ambiguity":
        return "medium"
    return "high"


def reasoning(process_title: str, cognitive_friction: str, capability_type: str) -> str:
    return f"{process_title} with {cognitive_friction} friction primarily needs {capability_type}."


def infer_confidence(capability_type: str, friction: str) -> float:
    direct_matches = {
        ("document_extraction", "unstructured_data"),
        ("classification", "routing"),
        ("entity_resolution", "reconciliation"),
        ("decision_support", "decision_ambiguity"),
    }
    if (capability_type, friction) in direct_matches:
        return 0.86
    return 0.72
