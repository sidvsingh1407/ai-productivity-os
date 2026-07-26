from typing import Dict, Any, Union
from pydantic import BaseModel
from models.ai_system import AISystem

# Base Score
DATA_SCORE_BASE = 100.0

# Penalties
SENSITIVITY_ACCESS_PENALTY = 25.0
STALE_DATA_PENALTY = 20.0
MISSING_OWNER_PENALTY = 15.0

def calculate_data_score(system: Union[AISystem, BaseModel, Dict[str, Any]]) -> float:
    """
    Calculates a 0-100 deterministic Data Score based on AI System data fields.
    data_quality_notes is excluded as it is a freeform text field and cannot be reliably scored.
    """
    if isinstance(system, dict):
        data_sensitivity = system.get("data_sensitivity", "not_specified")
        data_accessibility = system.get("data_accessibility", [])
        data_freshness = system.get("data_freshness", "unknown")
        data_owner = system.get("data_owner")
    else:
        data_sensitivity = getattr(system, "data_sensitivity", "not_specified")
        data_accessibility = getattr(system, "data_accessibility", []) or []
        data_freshness = getattr(system, "data_freshness", "unknown")
        data_owner = getattr(system, "data_owner", None)

    score = DATA_SCORE_BASE

    # 1. High Sensitivity with weak accessibility penalty
    # Assume 'public' or missing strict accessibility counts as weak controls for highly sensitive data
    if data_sensitivity and data_sensitivity.lower() in ['high', 'critical', 'restricted', 'sensitive']:
        if not data_accessibility or any(access.lower() in ['public', 'open', 'unrestricted'] for access in data_accessibility):
            score -= SENSITIVITY_ACCESS_PENALTY

    # 2. Stale data penalty
    if data_freshness and data_freshness.lower() in ['stale', 'outdated', 'static', 'unknown']:
        score -= STALE_DATA_PENALTY

    # 3. Missing owner penalty
    if not data_owner:
        score -= MISSING_OWNER_PENALTY

    # Clamp to 0-100
    return max(0.0, min(100.0, score))
