from typing import Dict, Any, List
from .industry_knowledge_base import INDUSTRY_KNOWLEDGE_BASE

def adapt_findings(findings: List[Dict[str, Any]], industry_type: str | None) -> List[Dict[str, Any]]:
    if not industry_type:
        return findings

    industry_data = INDUSTRY_KNOWLEDGE_BASE.get(industry_type.upper())
    if not industry_data:
        return findings

    adapted = []
    for finding in findings:
        new_finding = finding.copy()

        # In intelligence_engine.py we clean findings and remove 'type' / 'dimension'
        # We need a way to identify if it's governance, integration, etc.
        # We'll use title mapping for now, or assume the base pipeline provides it.
        # Let's check finding title or dimension if available.
        # Actually, base findings before cleaning have a "type" or "dimension" field, but in generate_intelligence we clean them up.
        # We'll adapt them based on title matching for simplicity, or we should adapt before cleaning.
        # Let's assume we adapt before cleaning, so 'dimension' might be present.

        dimension = new_finding.get("dimension")
        if not dimension:
            # Fallback title mapping if dimension is stripped
            title_lower = finding.get("title", "").lower()
            if "governance" in title_lower:
                dimension = "governance"
            elif "integration" in title_lower:
                dimension = "integration"

        if dimension:
            industry_finding = industry_data.get(f"{dimension}_finding")
            if industry_finding:
                new_finding["title"] = industry_finding.get("title", new_finding["title"])
                new_finding["impact"] = industry_finding.get("impact", new_finding["impact"])
                new_finding["rationale"] = industry_finding.get("rationale", new_finding["rationale"])

        adapted.append(new_finding)
    return adapted

def adapt_recommendations(recommendations: List[Dict[str, Any]], industry_type: str | None) -> List[Dict[str, Any]]:
    if not industry_type:
        return recommendations

    industry_data = INDUSTRY_KNOWLEDGE_BASE.get(industry_type.upper())
    if not industry_data:
        return recommendations

    adapted = []
    for rec in recommendations:
        new_rec = rec.copy()
        # Assume linked_finding or some way to identify dimension
        linked = new_rec.get("linked_finding", "")

        dimension = None
        if "governance" in linked:
            dimension = "governance"
        elif "integration" in linked:
            dimension = "integration"

        if dimension:
            industry_rec = industry_data.get(f"{dimension}_recommendation")
            if industry_rec:
                new_rec["recommendation"] = industry_rec.get("recommendation", new_rec["recommendation"])

        adapted.append(new_rec)
    return adapted

def adapt_executive_summary(summary: Dict[str, str], industry_type: str | None) -> Dict[str, str]:
    if not industry_type:
        return summary

    industry_data = INDUSTRY_KNOWLEDGE_BASE.get(industry_type.upper())
    if not industry_data:
        return summary

    new_summary = summary.copy()

    # We can inject some industry flavor into the overall assessment or risk
    # For now, if the critical risk mentions governance, we can swap it.
    critical_risk = new_summary.get("critical_risk", "")

    # Simple heuristic to adapt the critical risk text based on industry risk if it's a governance issue
    if "governance" in critical_risk.lower():
        gov_finding = industry_data.get("governance_finding")
        if gov_finding:
            new_summary["critical_risk"] = gov_finding["title"] + ": " + gov_finding["impact"]

    # Or adapt based on top risk
    risks = industry_data.get("risks", [])
    if risks and "governance" in critical_risk.lower():
        # Just an example of tailoring
        new_summary["critical_risk"] = f"Industry-specific vulnerability detected: {risks[0]}"

    return new_summary

def adapt_risk_projection(risk_projection: Dict[str, Any], industry_type: str | None) -> Dict[str, Any]:
    if not industry_type:
        return risk_projection

    industry_data = INDUSTRY_KNOWLEDGE_BASE.get(industry_type.upper())
    if not industry_data:
        return risk_projection

    new_proj = risk_projection.copy()

    # Append industry specific risks to risk drivers
    industry_risks = industry_data.get("risks", [])
    if industry_risks:
        # Prepend the top industry risk
        drivers = new_proj.get("risk_drivers", [])
        if drivers:
             new_proj["risk_drivers"] = [industry_risks[0]] + drivers[:2] # Keep top 3

    return new_proj
