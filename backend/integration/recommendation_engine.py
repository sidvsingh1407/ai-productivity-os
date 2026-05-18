from typing import List, Dict, Any
from .schemas import RecommendationItem

def get_priority(score: int) -> str:
    if score < 12:
        return "HIGH"
    elif score <= 16:
        return "MEDIUM"
    else:
        return "LOW"

def generate_recommendations(scores: Dict[str, Any], blueprints: List[Any], compliance_risk_flag: bool) -> List[RecommendationItem]:
    dimension_mapping = {
        "awareness": "training_processes",
        "adoption": "tool_integration",
        "integration": "workflow_automation",
        "governance": "compliance_processes",
        "roi": "measurement"
    }

    compliance_keywords = ["data_processing", "user_profiling", "automated_decision", "ai_governance"]

    recommendations = []

    for dimension, score in scores.items():
        if dimension not in dimension_mapping:
            continue

        mapped_category = dimension_mapping[dimension]
        priority = get_priority(score)

        for bp in blueprints:
            bp_data = bp.blueprint_data or {}
            process_categories = bp_data.get("process_categories", [])

            # case-insensitive substring match
            if any(mapped_category.lower() in category.lower() for category in process_categories):

                is_compliance_flagged = False
                rationale = f"Addresses {dimension} gap."

                if compliance_risk_flag and any(kw in (bp.process_id or "") for kw in compliance_keywords):
                    is_compliance_flagged = True
                    rationale += " ⚠️ EU AI Act compliance risk — review before implementation"

                recommendations.append(RecommendationItem(
                    blueprint_id=bp.id,
                    priority=priority,
                    rationale=rationale.strip(),
                    compliance_flagged=is_compliance_flagged,
                    dimension=dimension
                ))

    def sort_key(item: RecommendationItem):
        # Sorting order for recommendations:
        # 1st: HIGH priority AND compliance_flagged
        # 2nd: HIGH priority NOT compliance_flagged
        # 3rd: MEDIUM priority AND compliance_flagged
        # 4th: MEDIUM priority NOT compliance_flagged
        # 5th: LOW priority AND compliance_flagged
        # 6th: LOW priority NOT compliance_flagged

        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        # We want True to come before False, so False = 1, True = 0
        compliance_order = 0 if item.compliance_flagged else 1

        return (priority_order.get(item.priority, 3), compliance_order)

    recommendations.sort(key=sort_key)
    return recommendations
