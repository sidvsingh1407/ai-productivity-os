from typing import Dict, Any, List

# --- MAPPINGS & TAXONOMY ---
COI_TAXONOMY = {
    "AI Governance Framework Vulnerability": {
        "primary": "Governance Risk",
        "consequence": "AI initiatives evolve without consistent oversight or accountability.",
        "impact": "Increased policy inconsistency, fragmented decision-making, and elevated governance exposure.",
        "dimension": "governance"
    },
    "Systems Integration Bottleneck": {
        "primary": "Operational Risk",
        "consequence": "AI tools remain isolated from core workflows.",
        "impact": "Reduced efficiency gains and duplicated operational effort.",
        "dimension": "integration"
    },
    "Measurement & Value Tracking Gap": {
        "primary": "ROI Risk",
        "consequence": "Leadership cannot determine whether AI investments create value.",
        "impact": "Budget inefficiency and reduced executive confidence in AI initiatives.",
        "dimension": "roi"
    },
    "Localized & Informal AI Adoption": {
        "primary": "Adoption Risk",
        "consequence": "AI knowledge remains concentrated within isolated teams.",
        "impact": "Slow organizational adoption and inconsistent capability development.",
        "dimension": "adoption"
    },
    "Organizational Knowledge Silos": {
        "primary": "Adoption Risk",
        "consequence": "Successful AI practices are not shared across departments.",
        "impact": "Repeated effort and slower capability maturation.",
        "dimension": "adoption"
    },
    "Regulatory & Compliance Exposure": {
        "primary": "Compliance Risk",
        "consequence": "AI usage may violate internal or external compliance requirements.",
        "impact": "Regulatory scrutiny, audit findings, or reputational risk.",
        "dimension": "governance"
    },
    "Operational Contradictions Detected": {
        "primary": "Operational Risk",
        "consequence": "Reported practices do not align with operational reality.",
        "impact": "Decision-making based on incomplete or conflicting information.",
        "dimension": "special_contradictions"
    },
    "Structural Visibility Gaps": {
        "primary": "Operational Risk",
        "consequence": "Leadership lacks visibility into AI activity and outcomes.",
        "impact": "Reduced ability to govern, prioritize, and optimize initiatives.",
        "dimension": "special_visibility"
    }
}

def determine_risk_level(
    finding_title: str,
    severity: str,
    dimension_scores: Dict[str, int],
    contradiction_count: int,
    confidence_index: int
) -> str:
    """
    Determines the Risk Level for a specific finding based on:
    1. Finding Severity
    2. Dimension Score
    3. Confidence Index
    """
    mapping = COI_TAXONOMY.get(finding_title)
    if not mapping:
        # Fallback if unknown finding
        return "Medium"

    dim_key = mapping["dimension"]

    # Special Case: Operational Contradictions Detected
    if dim_key == "special_contradictions":
        if contradiction_count >= 5:
            base_risk = "Critical"
        elif contradiction_count >= 3:
            base_risk = "High"
        elif contradiction_count >= 1:
            base_risk = "Medium"
        else:
            base_risk = "Low"

        # Increase risk by one level if confidence < 50
        if confidence_index < 50:
            if base_risk == "High": return "Critical"
            if base_risk == "Medium": return "High"
            if base_risk == "Low": return "Medium"
        return base_risk

    # Special Case: Structural Visibility Gaps
    if dim_key == "special_visibility":
        dim_score = dimension_scores.get("integration", 100)
    else:
        # Normal findings
        dim_score = dimension_scores.get(dim_key, 100)

    # Standard Logic
    # Critical: Severity = Critical AND Score < 40
    if severity == "Critical" and dim_score < 40:
        base_risk = "Critical"
    # High: (Severity = Major AND Score < 50) OR (Severity = Critical AND Score >= 40)
    elif (severity == "Major" and dim_score < 50) or (severity == "Critical" and dim_score >= 40):
        base_risk = "High"
    # Medium: Severity = Moderate OR Score between 50-70
    elif severity == "Moderate" or (50 <= dim_score <= 70):
        base_risk = "Medium"
    # Low: Severity = Advisory AND Score > 70
    elif severity == "Advisory" and dim_score > 70:
        base_risk = "Low"
    else:
        # Fallback
        if severity == "Critical":
            base_risk = "Critical"
        elif severity == "Major":
            base_risk = "High"
        elif severity == "Moderate":
            base_risk = "Medium"
        else:
            base_risk = "Low"

    # Apply Confidence Modifier for Structural Visibility Gaps
    if dim_key == "special_visibility" and confidence_index < 50:
        if base_risk == "High": return "Critical"
        if base_risk == "Medium": return "High"
        if base_risk == "Low": return "Medium"

    return base_risk


def generate_cost_of_inaction(
    findings: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]],
    dimension_scores: Dict[str, int],
    contradiction_count: int,
    confidence_index: int
) -> List[Dict[str, Any]]:
    """
    Generates a deterministic Cost of Inaction list based on findings and scores.
    """
    coi_list = []

    # Create a lookup for recommendations by finding
    # Note: Currently the intelligence engine links findings to recommendations via 'linked_finding' internally.
    rec_lookup = {}
    for r in recommendations:
        if "linked_finding" in r:
            rec_lookup[r["linked_finding"]] = r["recommendation"]

    for finding in findings:
        title = finding.get("title")
        severity = finding.get("severity", "Advisory")

        # Don't generate COI for Advisory findings
        if severity == "Advisory" and title != "Structural Visibility Gaps":
            continue

        mapping = COI_TAXONOMY.get(title)
        if not mapping:
            continue

        risk_category = mapping["primary"]
        potential_consequence = mapping["consequence"]
        business_impact = mapping["impact"]

        risk_level = determine_risk_level(
            title,
            severity,
            dimension_scores,
            contradiction_count,
            confidence_index
        )

        related_rec = rec_lookup.get(title, "Conduct a detailed operational review to address this risk.")

        coi_list.append({
            "risk_category": risk_category,
            "risk_level": risk_level,
            "potential_consequence": potential_consequence,
            "business_impact": business_impact,
            "related_recommendation": related_rec
        })

    if not coi_list:
        # Positive-state handling for organizations with no findings
        coi_list.append({
            "risk_category": "Operational Resilience",
            "risk_level": "None",
            "potential_consequence": "No material operational risks identified based on current assessment data.",
            "business_impact": "Sustained operational efficiency and low risk exposure.",
            "related_recommendation": "Conduct periodic reassessments to maintain current operational resilience."
        })

    return coi_list