from typing import Dict, Any, Union
from pydantic import BaseModel
from models.ai_system import AISystem

# Additive Points Constants
DATA_OWNER_POINTS = 20.0
DATA_SENSITIVITY_POINTS = 20.0
DATA_FRESHNESS_POINTS = 20.0
DATA_ACCESSIBILITY_POINTS = 20.0
DATA_TYPES_SOURCES_POINTS = 20.0

def calculate_data_score(system: Union[AISystem, BaseModel, Dict[str, Any]]) -> float:
    """
    Calculates a 0-100 deterministic Data Score based on AI System data fields.
    This uses an additive model rewarding complete governance documentation rather than penalizing known-bad values.
    """
    if isinstance(system, dict):
        data_sensitivity = system.get("data_sensitivity")
        data_accessibility = system.get("data_accessibility")
        data_freshness = system.get("data_freshness")
        data_owner = system.get("data_owner")
        data_types = system.get("data_types")
        data_sources = system.get("data_sources")
    else:
        data_sensitivity = getattr(system, "data_sensitivity", None)
        data_accessibility = getattr(system, "data_accessibility", None)
        data_freshness = getattr(system, "data_freshness", None)
        data_owner = getattr(system, "data_owner", None)
        data_types = getattr(system, "data_types", None)
        data_sources = getattr(system, "data_sources", None)

    score = 0.0

    if data_owner and isinstance(data_owner, str) and data_owner.strip():
        score += DATA_OWNER_POINTS

    if data_sensitivity and isinstance(data_sensitivity, str) and data_sensitivity.strip():
        score += DATA_SENSITIVITY_POINTS

    if data_freshness and isinstance(data_freshness, str) and data_freshness.strip():
        score += DATA_FRESHNESS_POINTS

    if data_accessibility and isinstance(data_accessibility, list) and len(data_accessibility) > 0:
        score += DATA_ACCESSIBILITY_POINTS

    # Award points if either data_types or data_sources are meaningfully populated
    has_types = data_types and isinstance(data_types, list) and len(data_types) > 0
    has_sources = data_sources and isinstance(data_sources, list) and len(data_sources) > 0
    if has_types or has_sources:
        score += DATA_TYPES_SOURCES_POINTS

    # Clamp to 0-100 just in case
    return max(0.0, min(100.0, score))
