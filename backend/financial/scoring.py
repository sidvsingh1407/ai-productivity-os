from typing import Dict, Any, Union, Optional
from pydantic import BaseModel
from models.ai_system import AISystem
from financial.calculator import calculate_system_cost

def calculate_roi_score(system: Union[AISystem, BaseModel, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates ROI score.
    Since expected_benefits is a freeform text field, true ROI cannot be calculated deterministically.
    Returns None for the score with a documented reason, alongside the cost partial data indicators.
    """
    cost_data = calculate_system_cost(system)

    return {
        "roi_score": None,
        "roi_score_unavailable_reason": "expected_benefits is not a structured numeric field",
        "cost_is_partial": cost_data.get("is_partial", False),
        "cost_missing_components": cost_data.get("missing_components", [])
    }
