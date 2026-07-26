from typing import Dict, Any, Union
from pydantic import BaseModel
from models.adoption_record import AdoptionRecord

# Constants for Thresholds and Weights
# User Count Base Points
USER_COUNT_THRESHOLDS = [
    (100, 100.0),
    (50, 75.0),
    (10, 50.0),
    (0, 25.0),
]
USER_COUNT_ZERO_SCORE = 0.0

# Usage Frequency Modifiers
USAGE_FREQ_MODIFIER = {
    'daily': 1.2,
    'weekly': 1.0,
    'monthly': 0.8,
    'rare': 0.5,
    'not_specified': 1.0
}

# Penalties and Bonuses (additive/subtractive)
SHADOW_AI_PENALTY = 20.0

RESISTANCE_LEVEL_PENALTY = {
    'low': 0.0,
    'medium': 15.0,
    'high': 30.0,
    'not_specified': 0.0
}

TRAINING_STATUS_BONUS = {
    'completed': 20.0,
    'in_progress': 10.0,
    'planned': 5.0,
    'none': 0.0,
    'not_specified': 0.0
}

def calculate_adoption_score(record: Union[AdoptionRecord, BaseModel, Dict[str, Any]]) -> float:
    """
    Calculates a 0-100 deterministic Adoption Score.
    """
    if isinstance(record, dict):
        user_count = record.get("user_count", 0)
        usage_frequency = record.get("usage_frequency", "not_specified")
        shadow_ai_detected = record.get("shadow_ai_detected", False)
        resistance_level = record.get("resistance_level", "not_specified")
        training_status = record.get("training_status", "not_specified")
    else:
        user_count = getattr(record, "user_count", 0)
        usage_frequency = getattr(record, "usage_frequency", "not_specified")
        shadow_ai_detected = getattr(record, "shadow_ai_detected", False)
        resistance_level = getattr(record, "resistance_level", "not_specified")
        training_status = getattr(record, "training_status", "not_specified")

    # 1. Base Score from User Count
    base_score = USER_COUNT_ZERO_SCORE
    if user_count > 0:
        for threshold, points in USER_COUNT_THRESHOLDS:
            if user_count > threshold:
                base_score = points
                break

    # 2. Apply Usage Frequency Multiplier
    multiplier = USAGE_FREQ_MODIFIER.get(usage_frequency, 1.0)
    score = base_score * multiplier

    # 3. Apply Penalties
    if shadow_ai_detected:
        score -= SHADOW_AI_PENALTY

    score -= RESISTANCE_LEVEL_PENALTY.get(resistance_level, 0.0)

    # 4. Apply Bonuses
    score += TRAINING_STATUS_BONUS.get(training_status, 0.0)

    # 5. Clamp to 0-100
    return max(0.0, min(100.0, score))
