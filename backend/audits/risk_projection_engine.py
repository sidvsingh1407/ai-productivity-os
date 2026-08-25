from typing import Dict, Any, List

def calculate_risk_score(dimension_scores: Dict[str, int], missing_data: List[str]) -> int:
    """
    Calculates a risk score from 0-100 based on weighted maturity gaps.
    Higher risk score -> Higher risk.
    """
    gov_score = dimension_scores.get('governance', 100)
    adoption_score = dimension_scores.get('adoption', 100)
    integration_score = dimension_scores.get('integration', 100)
    roi_score = dimension_scores.get('roi', 100)

    base_risk = (
        (100 - gov_score) * 0.35 +
        (100 - adoption_score) * 0.20 +
        (100 - integration_score) * 0.20 +
        (100 - roi_score) * 0.15
    )

    missing_data_count = len(missing_data)
    visibility_penalty = min(10, missing_data_count * 2)

    final_risk = min(100, int(base_risk + visibility_penalty))
    return final_risk

def determine_risk_level(risk_score: int) -> str:
    """
    Determines risk level based on the calculated risk score.
    """
    if risk_score >= 70:
        return "Critical"
    if risk_score >= 55:
        return "High"
    if risk_score >= 40:
        return "Elevated"
    if risk_score >= 20:
        return "Moderate"
    return "Low"



def generate_risk_explanation(risk_score: int, risk_level: str, dimension_scores: Dict[str, int], missing_data_count: int) -> str:
    reasons = []

    # Check lowest dimensions
    sorted_dims = sorted(dimension_scores.items(), key=lambda item: item[1])
    if sorted_dims:
        lowest_dim = sorted_dims[0]
        if lowest_dim[1] < 50:
             reasons.append(f"{lowest_dim[0].capitalize()} score is below threshold")
        elif lowest_dim[1] < 75:
             reasons.append(f"{lowest_dim[0].capitalize()} maturity is moderate")

    if missing_data_count > 0:
        if missing_data_count == 1:
             reasons.append("1 missing data flag reduces confidence")
        else:
             reasons.append(f"{missing_data_count} missing data flags reduce confidence")

    if not reasons:
         return f"Risk is {risk_level.lower()} as maturity levels are generally strong."

    explanation = f"Risk is {risk_level.lower()} because "
    if len(reasons) == 1:
        explanation += reasons[0].lower() + "."
    elif len(reasons) == 2:
        explanation += reasons[0].lower() + " and " + reasons[1].lower() + "."
    else:
        explanation += ", ".join(r.lower() for r in reasons[:-1]) + ", and " + reasons[-1].lower() + "."

    return explanation

def calculate_confidence_score(missing_data_count: int, contradiction_count: int, eqs: int) -> int:
    confidence = 100
    confidence -= (missing_data_count * 10)
    confidence -= (contradiction_count * 10)
    if eqs < 50:
        confidence -= 15
    return max(0, min(100, confidence))

def generate_risk_drivers(dimension_scores: Dict[str, int]) -> List[str]:
    """
    Extracts top 3-5 risk drivers based on lowest dimension scores.
    """
    drivers = []
    # Sort dimensions by score ascending (lowest first)
    sorted_dims = sorted(dimension_scores.items(), key=lambda item: item[1])

    driver_mapping = {
        'governance': "Governance maturity gap",
        'integration': "Integration maturity gap",
        'roi': "ROI measurement gap",
        'awareness': "Awareness and readiness gap",
        'adoption': "Adoption consistency gap"
    }

    for dim, score in sorted_dims:
        if score < 75 and dim in driver_mapping:
            drivers.append(driver_mapping[dim])

        if len(drivers) >= 3:
            break

    # Ensure at least one driver if scores are moderately low, or empty if perfect
    if not drivers and any(score < 90 for score in dimension_scores.values()):
        lowest_dim = sorted_dims[0][0]
        if lowest_dim in driver_mapping:
            drivers.append(driver_mapping[lowest_dim])

    return drivers

def generate_risk_timeline(dimension_scores: Dict[str, int]) -> Dict[str, List[str]]:
    """
    Projects consequences at Near-Term, Mid-Term, and Long-Term intervals.
    """
    timeline = {
        "near_term": [],
        "mid_term": [],
        "long_term": []
    }

    # Identify weakest dimensions
    weakest_dims = [dim for dim, score in dimension_scores.items() if score < 70]

    # Near-Term (0-3 Months)
    if 'adoption' in weakest_dims or 'awareness' in weakest_dims:
        timeline["near_term"].append("Operational inefficiencies expand due to uncoordinated usage.")
    elif len(weakest_dims) > 0:
        timeline["near_term"].append("Initial operational friction increases.")

    # Mid-Term (3-12 Months)
    if 'governance' in weakest_dims:
        timeline["mid_term"].append("Governance and adoption gaps begin affecting execution quality.")
    if 'integration' in weakest_dims:
        timeline["mid_term"].append("System bottlenecks prevent scaling of initial successes.")
    if not timeline["mid_term"] and len(weakest_dims) > 0:
        timeline["mid_term"].append("Maturity gaps begin affecting execution quality.")

    # Long-Term (12+ Months)
    if 'roi' in weakest_dims:
        timeline["long_term"].append("Strategic value realization becomes increasingly difficult.")
    if 'governance' in weakest_dims:
        timeline["long_term"].append("Significant compliance and shadow IT risks materialize.")
    if not timeline["long_term"] and len(weakest_dims) > 0:
        timeline["long_term"].append("AI investments fail to generate measurable returns.")

    return timeline

def generate_risk_projection(scores: Dict[str, Any], findings: List[Dict[str, Any]], risk_trend: str = "Stable") -> Dict[str, Any]:
    """
    Orchestrates the generation of the risk projection payload.
    """
    raw_dimensions = scores.get('dimensions', {})
    dimension_scores = {k: v * 5 for k, v in raw_dimensions.items()}

    missing_data = scores.get('missing_data_flags', [])
    contradictions = scores.get('contradictions', [])
    eqs = scores.get('evidence_quality_score', 100)

    risk_score = calculate_risk_score(dimension_scores, missing_data)
    risk_level = determine_risk_level(risk_score)
    confidence = calculate_confidence_score(len(missing_data), len(contradictions), eqs)

    # risk_trend is now passed in from the caller

    explanation = generate_risk_explanation(risk_score, risk_level, dimension_scores, len(missing_data))

    risk_drivers = generate_risk_drivers(dimension_scores)
    risk_timeline = generate_risk_timeline(dimension_scores)

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_trend": risk_trend,
        "confidence": confidence,
        "explanation": explanation,
        "risk_drivers": risk_drivers,
        "risk_timeline": risk_timeline
    }
