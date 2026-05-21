from __future__ import annotations


ALLOWED_FRICTION_TYPES = {"unstructured_data", "reconciliation", "routing", "decision_ambiguity"}
ALLOWED_FRICTION_SEVERITIES = {"low", "medium", "high"}
ALLOWED_HITL_NEEDS = {"none", "validation", "decision"}


def diagnose_workflow_friction(normalized_text: str) -> dict[str, object]:
    text = normalized_text.lower()
    friction_type = primary_friction_type(text)
    hitl_need = infer_hitl_need(text, friction_type)
    severity = infer_severity(text, hitl_need)
    confidence = infer_confidence(text, friction_type)
    return {
        "cognitive_friction": friction_type,
        "friction_severity": severity,
        "mechanical_friction": infer_mechanical_friction(text),
        "hitl_need": hitl_need,
        "confidence": confidence,
    }


def primary_friction_type(text: str) -> str:
    if any(word in text for word in ["reconcile", "reconciliation", "match", "matching", "discrepancy", "cross-reference"]):
        return "reconciliation"
    if any(word in text for word in ["route", "routing", "triage", "queue", "priority", "ticket"]):
        return "routing"
    if any(word in text for word in ["approval", "exception", "risk", "decision", "review", "compliance", "legal"]):
        return "decision_ambiguity"
    return "unstructured_data"


def infer_severity(text: str, hitl_need: str) -> str:
    high_signals = ["compliance", "legal", "audit", "financial", "healthcare", "security", "pii", "discrepancy"]
    medium_signals = ["approval", "manual", "review", "match", "route", "reconciliation", "extract"]
    if hitl_need == "decision" or any(signal in text for signal in high_signals):
        return "high"
    if hitl_need == "validation" or any(signal in text for signal in medium_signals):
        return "medium"
    return "low"


def infer_mechanical_friction(text: str) -> str:
    if any(word in text for word in ["erp", "crm", "sap", "workday", "writeback", "copy", "paste", "rekey"]):
        return "manual system writeback"
    if any(word in text for word in ["email", "slack", "teams", "notify", "reminder", "followup"]):
        return "manual notification and follow-up"
    if any(word in text for word in ["route", "queue", "ticket"]):
        return "manual queue routing"
    return ""


def infer_hitl_need(text: str, friction_type: str) -> str:
    if any(word in text for word in ["approval", "exception", "legal", "compliance", "risk", "audit", "security"]):
        return "decision"
    if friction_type in {"reconciliation", "decision_ambiguity"}:
        return "validation"
    return "none"


def infer_confidence(text: str, friction_type: str) -> float:
    signal_groups = {
        "unstructured_data": ["pdf", "document", "email", "form", "extract", "unstructured"],
        "reconciliation": ["reconcile", "reconciliation", "match", "matching", "discrepancy", "cross-reference"],
        "routing": ["route", "routing", "triage", "queue", "priority", "ticket"],
        "decision_ambiguity": ["approval", "exception", "risk", "decision", "review", "compliance", "legal"],
    }
    hits = sum(1 for signal in signal_groups[friction_type] if signal in text)
    return round(min(0.95, max(0.58, 0.58 + hits * 0.08)), 4)
