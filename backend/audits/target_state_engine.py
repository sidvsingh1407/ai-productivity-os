from typing import Dict, Any, List

# Rationale Matrix: Dimension -> Priority -> Narrative
RATIONALE_MATRIX = {
    "governance": {
        "High": "Governance maturity is insufficient to support scaled AI adoption and introduces elevated operational and compliance risk.",
        "Medium": "Governance structures exist but require formalization to consistently manage AI risks across expanding use cases.",
        "Low": "Governance frameworks are well-established; focus on continuous optimization and adapting to emerging regulatory standards."
    },
    "roi": {
        "High": "Current AI initiatives lack measurable value realization mechanisms, limiting executive confidence and future investment.",
        "Medium": "Initial ROI metrics are tracked, but a comprehensive financial and operational value realization framework is needed for scale.",
        "Low": "Strong value realization practices are in place; optimize by expanding measurement to strategic secondary benefits."
    },
    "awareness": {
        "High": "A critical lack of AI awareness creates substantial resistance and prevents the organization from identifying valuable use cases.",
        "Medium": "Awareness levels support experimentation but are unlikely to sustain organization-wide adoption without structured enablement.",
        "Low": "High AI literacy exists across the organization; shift focus to advanced capability training and specialized use cases."
    },
    "integration": {
        "High": "Core systems lack the structural readiness for AI, creating severe bottlenecks that prevent automated data flow.",
        "Medium": "Partial integrations support isolated workflows, but deeper architectural alignment is required for scalable automation.",
        "Low": "Systems are well-integrated; prioritize advanced API orchestrations and real-time data optimizations."
    },
    "adoption": {
        "High": "Adoption is fragmented or non-existent, leading to inconsistent productivity and elevated shadow IT risks.",
        "Medium": "Localized adoption is successful, but standardized playbooks are necessary to replicate gains across the enterprise.",
        "Low": "Widespread, formalized adoption is present; focus on accelerating advanced tooling and continuous process improvement."
    }
}

def generate_target_state(scores_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates the Current State vs Target State for every completed AI Audit.
    Transforms raw dimension scores into a maturity roadmap representation.
    """
    target_state = []

    dimensions = scores_dict.get('dimension_scores')
    if dimensions is None:
        # Fallback: Scale dimensions by 5 if only raw dimensions are present (since raw scores are 0-20)
        dimensions = {k: v * 5 for k, v in scores_dict.get('dimensions', {}).items()}

    for dimension, current_score in dimensions.items():
        # Calculate target score using a deterministic maturity-improvement formula
        gap_to_ideal = 100 - current_score

        # Improvement factor rules
        if current_score < 40:
            improvement_factor = 0.6
        elif current_score < 60:
            improvement_factor = 0.5
        elif current_score < 80:
            improvement_factor = 0.4
        else:
            improvement_factor = 0.3

        target_score_float = current_score + (gap_to_ideal * improvement_factor)
        target_score = round(target_score_float)

        # Calculate gap
        gap = target_score - current_score

        # Determine improvement priority
        if gap >= 40:
            priority = "High"
        elif gap >= 20:
            priority = "Medium"
        else:
            priority = "Low"

        # Get rationale
        rationale = RATIONALE_MATRIX.get(dimension.lower(), {}).get(priority, "Improvement is required to achieve target maturity.")

        # Format dimension name (e.g. "governance" -> "Governance", "roi" -> "ROI")
        dimension_name = "ROI" if dimension.lower() == "roi" else dimension.capitalize()

        target_state.append({
            "dimension": dimension_name,
            "current_score": current_score,
            "target_score": target_score,
            "gap": gap,
            "improvement_priority": priority,
            "rationale": rationale
        })

    return target_state
