from typing import List, Dict, Any

def generate_workflow_recommendations(opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Consumes a list of opportunities and generates workflow recommendations deterministically.
    """
    recommendations = []

    # Deterministic mapping
    category_mapping = {
        "manual_work": "automation",
        "repetitive_decisions": "decision_support",
        "knowledge_bottleneck": "rag",
        "customer_pain": "ai_copilot",
        "department_pain": "analytics",
        "automation_candidate": "predictive_models"
    }

    for opp in opportunities:
        org_id = opp["organization_id"]
        opp_id = opp["id"]
        category = opp["category"]
        title = opp["title"]
        priority = opp["confidence_or_priority"]

        recommendation_type = category_mapping.get(category)

        if recommendation_type:
            rationale = f"Recommended {recommendation_type} workflow to address {category} opportunity ({priority} priority): {title}"

            recommendations.append({
                "organization_id": org_id,
                "opportunity_id": opp_id,
                "agent_recommendation_id": None, # Intentionally left unpopulated
                "recommendation_type": recommendation_type,
                "rationale": rationale,
                "confidence": priority  # Reusing confidence_or_priority from opportunity
            })

    return recommendations
