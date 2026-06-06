from typing import Dict, Any, List

# --- MAPPINGS & TAXONOMY ---
COI_TAXONOMY = {
    "AI Governance Framework Vulnerability": {
        "primary": "Governance Risk",
        "consequence": "AI initiatives evolve without consistent oversight or accountability.",
        "impact": "Increased policy inconsistency, fragmented decision-making, and elevated governance exposure.",
        "dimension": "governance",
        "deterioration_rate": 15
    },
    "Systems Integration Bottleneck": {
        "primary": "Operational Risk",
        "consequence": "AI tools remain isolated from core workflows.",
        "impact": "Reduced efficiency gains and duplicated operational effort.",
        "dimension": "integration",
        "deterioration_rate": 10
    },
    "Measurement & Value Tracking Gap": {
        "primary": "ROI Risk",
        "consequence": "Leadership cannot determine whether AI investments create value.",
        "impact": "Budget inefficiency and reduced executive confidence in AI initiatives.",
        "dimension": "roi",
        "deterioration_rate": 12
    },
    "Localized & Informal AI Adoption": {
        "primary": "Adoption Risk",
        "consequence": "AI knowledge remains concentrated within isolated teams.",
        "impact": "Slow organizational adoption and inconsistent capability development.",
        "dimension": "adoption",
        "deterioration_rate": 8
    },
    "Organizational Knowledge Silos": {
        "primary": "Adoption Risk",
        "consequence": "Successful AI practices are not shared across departments.",
        "impact": "Repeated effort and slower capability maturation.",
        "dimension": "adoption",
        "deterioration_rate": 8
    },
    "Regulatory & Compliance Exposure": {
        "primary": "Compliance Risk",
        "consequence": "AI usage may violate internal or external compliance requirements.",
        "impact": "Regulatory scrutiny, audit findings, or reputational risk.",
        "dimension": "governance",
        "deterioration_rate": 20
    },
    "Operational Contradictions Detected": {
        "primary": "Operational Risk",
        "consequence": "Reported practices do not align with operational reality.",
        "impact": "Decision-making based on incomplete or conflicting information.",
        "dimension": "special_contradictions",
        "deterioration_rate": 15
    },
    "Structural Visibility Gaps": {
        "primary": "Operational Risk",
        "consequence": "Leadership lacks visibility into AI activity and outcomes.",
        "impact": "Reduced ability to govern, prioritize, and optimize initiatives.",
        "dimension": "special_visibility",
        "deterioration_rate": 15
    }
}

def determine_base_dimension_risk(dim_score: int) -> int:
    """
    Converts a dimension score (0-100) into a base risk score (0-100).
    """
    return 100 - dim_score

def generate_cost_of_inaction(
    findings: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]],
    dimension_scores: Dict[str, int],
    contradiction_count: int,
    confidence_index: int
) -> List[Dict[str, Any]]:
    """
    Generates a deterministic Cost of Inaction list based on findings and scores,
    including quantitative risk projections.
    """
    coi_list = []

    # Create a lookup for recommendations by finding
    rec_lookup = {}
    for r in recommendations:
        if "linked_finding" in r:
            rec_lookup[r["linked_finding"]] = r["recommendation"]

    for finding in findings:
        title = finding.get("title")
        severity = finding.get("severity", "Advisory")

        # Don't generate COI for Advisory findings unless it's a specific visibility gap
        if severity == "Advisory" and title != "Structural Visibility Gaps":
            continue

        mapping = COI_TAXONOMY.get(title)
        if not mapping:
            continue

        risk_category = mapping["primary"]
        dim_key = mapping["dimension"]

        if dim_key == "special_contradictions" or dim_key == "special_visibility":
            # For special risks without a single dimension, map to overall risk or a proxy
            dim_score = dimension_scores.get("governance", 50) # Fallback to gov or middle
        else:
            dim_score = dimension_scores.get(dim_key, 100)

        current_risk = determine_base_dimension_risk(dim_score)

        # Determine 12-month projection based on deterioration rate
        deterioration = mapping.get("deterioration_rate", 10)

        # Aggravate deterioration if confidence is low or severity is critical
        if severity == "Critical":
            deterioration += 5
        if confidence_index < 60:
            deterioration += 5

        projected_12m_risk = min(100, current_risk + deterioration)
        risk_change = f"+{projected_12m_risk - current_risk}"

        expected_impact = [mapping["consequence"], mapping["impact"]]

        related_rec = rec_lookup.get(title, "Conduct a detailed operational review to address this risk.")

        coi_list.append({
            "risk_category": risk_category,
            "current_risk": current_risk,
            "projected_12m_risk": projected_12m_risk,
            "risk_change": risk_change,
            "expected_impact": expected_impact,
            "related_recommendation": related_rec
        })

    if not coi_list:
        # Positive-state handling for organizations with no findings
        coi_list.append({
            "risk_category": "Operational Resilience",
            "current_risk": 10,
            "projected_12m_risk": 10,
            "risk_change": "+0",
            "expected_impact": [
                "No material operational risks identified based on current assessment data.",
                "Sustained operational efficiency and low risk exposure."
            ],
            "related_recommendation": "Conduct periodic reassessments to maintain current operational resilience."
        })

    return coi_list
