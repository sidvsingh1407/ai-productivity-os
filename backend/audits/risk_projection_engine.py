from typing import Dict, Any, List

def calculate_risk_score(total_score: int, dimension_scores: Dict[str, int]) -> int:
    """
    Calculates a risk score from 0-100 based on weighted maturity gaps.
    Lower total_score -> Higher risk.
    """
    # Assuming total_score is out of 100
    base_risk = 100 - total_score

    # Add penalty for critical dimension gaps (e.g. Governance < 50)
    penalty = 0
    gov_score = dimension_scores.get('governance', 100)
    if gov_score < 50:
        penalty += (50 - gov_score) * 0.5

    final_risk = min(100, max(0, int(base_risk + penalty)))
    return final_risk

def determine_risk_level(total_score: int, dimension_scores: Dict[str, int], findings: List[Dict[str, Any]], compliance_risk: bool, missing_data: List[str], contradictions: List[str]) -> str:
    """
    Determines risk level based on deterministic rules.
    """
    gov_score = dimension_scores.get('governance', 100)
    critical_findings_count = sum(1 for f in findings if f.get('severity') == 'Critical')
    major_findings_count = sum(1 for f in findings if f.get('severity') == 'High')

    # Critical
    if (total_score < 40 or
        gov_score < 35 or
        critical_findings_count >= 3 or
        (compliance_risk and gov_score < 50) or
        len(missing_data) >= 2):
        return "Critical"

    # High
    if (total_score < 60 or
        gov_score < 50 or
        major_findings_count >= 2 or
        len(contradictions) >= 2):
        return "High"

    # Moderate
    if (total_score < 80 or
        gov_score < 75 or
        major_findings_count >= 1):
        return "Moderate"

    # Low
    return "Low"

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

def generate_risk_projection(scores: Dict[str, Any], findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Orchestrates the generation of the risk projection payload.
    """
    # Extract total_score and dimension_scores. Assuming scores inside dimension_scores are out of 20, scaling to 100.
    raw_dimensions = scores.get('dimensions', {})
    dimension_scores = {k: v * 5 for k, v in raw_dimensions.items()}

    # sum(raw_dimensions.values()) is already out of 100 (5 dimensions * max 20).
    total_score = sum(raw_dimensions.values()) if raw_dimensions else scores.get('total_score', 0)

    compliance_risk = scores.get('compliance_risk_flag', False)
    missing_data = scores.get('missing_data_flags', [])
    contradictions = scores.get('contradictions', [])

    risk_level = determine_risk_level(total_score, dimension_scores, findings, compliance_risk, missing_data, contradictions)
    risk_score = calculate_risk_score(total_score, dimension_scores)
    risk_drivers = generate_risk_drivers(dimension_scores)
    risk_timeline = generate_risk_timeline(dimension_scores)

    # Determine confidence loosely based on missing data or contradiction flags
    confidence = 100
    if missing_data:
        confidence -= 10 * len(missing_data)
    if contradictions:
        confidence -= 10 * len(contradictions)
    confidence = max(0, confidence)

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "confidence": confidence,
        "risk_drivers": risk_drivers,
        "risk_timeline": risk_timeline
    }
