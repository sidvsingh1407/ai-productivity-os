from typing import Dict, Any, List

def generate_early_warnings(
    dimension_scores: Dict[str, int],
    missing_data: List[str],
    evidence_quality_score: int,
    contradictions: List[str]
) -> List[Dict[str, str]]:
    """
    Generates deterministic proactive early warnings based on maturity gaps, visibility, and evidence quality.
    Returns a list of dictionaries with warning, severity, and suggested action.
    """
    warnings = []

    # 1. Governance Deterioration
    gov_score = dimension_scores.get('governance', 100)
    if gov_score < 40:
        warnings.append({
            "warning": "Critical Governance Deficit",
            "severity": "High",
            "suggested_action": "Immediately establish an interim AI oversight committee."
        })
    elif gov_score < 60:
        warnings.append({
            "warning": "Governance Deterioration",
            "severity": "Medium",
            "suggested_action": "Review and update AI usage policies."
        })

    # 2. Low Adoption Velocity (Adoption < Integration)
    adoption_score = dimension_scores.get('adoption', 100)
    integration_score = dimension_scores.get('integration', 100)
    if adoption_score < integration_score - 20:
        warnings.append({
            "warning": "Low Adoption Velocity",
            "severity": "Medium",
            "suggested_action": "Invest in user training and change management."
        })

    # 3. Visibility Gaps
    if len(missing_data) >= 3:
        warnings.append({
            "warning": "Severe Visibility Gap",
            "severity": "High",
            "suggested_action": "Audit current AI inventory and standardize reporting."
        })
    elif len(missing_data) >= 1:
        warnings.append({
            "warning": "Emerging Visibility Gap",
            "severity": "Medium",
            "suggested_action": "Address missing assessment data points."
        })

    # 4. Poor ROI Trajectory
    roi_score = dimension_scores.get('roi', 100)
    if roi_score < 50 and gov_score < 50:
        warnings.append({
            "warning": "Poor ROI Trajectory",
            "severity": "High",
            "suggested_action": "Halt further scaling until measurement mechanisms are in place."
        })

    # 5. Low Evidence Quality / Contradictions
    if evidence_quality_score < 50 or len(contradictions) >= 2:
        warnings.append({
            "warning": "Assessment Reliability Risk",
            "severity": "High",
            "suggested_action": "Conduct a manual validation of self-reported maturity metrics."
        })

    return warnings
