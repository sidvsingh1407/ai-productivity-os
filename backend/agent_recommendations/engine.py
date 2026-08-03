from typing import List, Dict, Any, Optional

def normalize_department(dept: Optional[str]) -> Optional[str]:
    """
    Normalizes a free-text department string into a standard agent department key.
    Uses lowercase and substring/keyword matching.
    """
    if not dept:
        return None

    d = dept.lower()

    if any(k in d for k in ["hr", "human resources", "talent", "people"]):
        return "hr_agent"
    if any(k in d for k in ["sales", "revenue"]):
        return "sales_agent"
    if any(k in d for k in ["legal", "counsel", "law"]):
        return "legal_agent"
    if any(k in d for k in ["finance", "accounting", "treasury", "tax"]):
        return "finance_agent"
    if any(k in d for k in ["procurement", "supply chain", "purchasing", "sourcing", "vendor"]):
        return "procurement_agent"
    if any(k in d for k in ["support", "customer success", "cx", "customer support"]):
        return "customer_support_agent"

    return None

def generate_agent_recommendations(opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Consumes a list of opportunities (with 'department' joined from AISystem).
    Returns a list of agent recommendations (dicts).
    """
    recommendations = []

    for opp in opportunities:
        org_id = opp["organization_id"]
        opp_id = opp["id"]
        category = opp["category"]
        title = opp["title"]
        priority = opp["confidence_or_priority"]
        dept = opp.get("department")

        normalized_dept_agent = normalize_department(dept)
        agent_type = None

        if normalized_dept_agent:
            # Department specified and recognized
            if category == "knowledge_bottleneck":
                agent_type = "knowledge_agent"
            elif category == "customer_pain":
                agent_type = "customer_support_agent"
            else:
                agent_type = normalized_dept_agent
        else:
            # Org-level or unrecognized department
            if category == "knowledge_bottleneck":
                agent_type = "knowledge_agent"
            elif category == "customer_pain":
                agent_type = "customer_support_agent"
            else:
                agent_type = "executive_agent"

        if agent_type:
            rationale = f"Recommended {agent_type} to address {category} opportunity ({priority} priority): {title}"

            recommendations.append({
                "organization_id": org_id,
                "opportunity_id": opp_id,
                "agent_type": agent_type,
                "rationale": rationale,
                "confidence": priority  # reusing the same priority schema for confidence per requirements
            })

    return recommendations
