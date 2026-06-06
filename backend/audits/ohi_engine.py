from typing import Dict, Any

def calculate_ohi(dimension_scores: Dict[str, int], risk_score: int, evidence_quality_score: int) -> int:
    """
    Calculates the Operational Health Index (OHI) from 0-100.
    Weights:
    - Governance: 30%
    - Inverse Risk Score: 30%
    - Integration: 15%
    - Adoption: 10%
    - ROI: 10%
    - Awareness: 5%

    Evidence Quality acts as a modifier constraint on the final index.
    """
    gov_score = dimension_scores.get('governance', 100)
    integration_score = dimension_scores.get('integration', 100)
    adoption_score = dimension_scores.get('adoption', 100)
    roi_score = dimension_scores.get('roi', 100)
    awareness_score = dimension_scores.get('awareness', 100)

    inverse_risk = 100 - risk_score

    base_ohi = (
        (gov_score * 0.30) +
        (inverse_risk * 0.30) +
        (integration_score * 0.15) +
        (adoption_score * 0.10) +
        (roi_score * 0.10) +
        (awareness_score * 0.05)
    )

    # Evidence quality modifier (if quality is low, health cannot be definitively high)
    # If eqs < 50, OHI cannot exceed eqs + 20
    # If eqs < 30, OHI is capped heavily
    final_ohi = int(base_ohi)

    if evidence_quality_score < 70:
        penalty = (70 - evidence_quality_score) * 0.25 # up to 17.5 penalty
        final_ohi -= int(penalty)

    return max(0, min(100, final_ohi))

def generate_ohi_explanation(ohi: int, evidence_quality_score: int) -> str:
    """
    Generates a deterministic explanation for the OHI calculation.
    """
    explanation = f"Operational Health Index is {ohi}/100. "

    if ohi >= 80:
        explanation += "Health is optimized, driven by strong governance and low risk."
    elif ohi >= 60:
        explanation += "Health is managed but faces moderate friction in execution."
    elif ohi >= 40:
        explanation += "Health is vulnerable due to significant governance and operational gaps."
    else:
        explanation += "Health is critical. Systemic risks and structural gaps severely impair operations."

    if evidence_quality_score < 50:
        explanation += " Note: The score is constrained due to low assessment evidence quality."

    return explanation
