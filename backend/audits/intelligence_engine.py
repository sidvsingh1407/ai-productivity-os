from typing import Dict, Any, List
from audits.intelligence_rules import (
    determine_severity,
    determine_priority,
    DIMENSION_IMPACT,
    DIMENSION_EFFORT,
    FINDING_TEMPLATES,
    RECOMMENDATION_TEMPLATES,
    COMPLIANCE_FINDING,
    CONTRADICTION_FINDING,
    MISSING_DATA_FINDING
)
from audits.target_state_engine import generate_target_state
from audits.roadmap_engine import generate_roadmap
from audits.risk_projection_engine import generate_risk_projection
from audits.coi_engine import generate_cost_of_inaction
from failure_intelligence import detect_failure_patterns
from .industry_intelligence_engine import adapt_findings, adapt_recommendations, adapt_executive_summary, adapt_risk_projection

def generate_findings(scores: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates structured findings based on assessment scores.
    """
    findings = []

    # 1. Dimension-based findings
    dimensions = scores.get('dimensions', {})
    for dim_name, raw_score in dimensions.items():
        score_100 = raw_score * 5 # Convert from 20 to 100
        severity = determine_severity(score_100)

        # Only generate findings for actionable severities (or all if requested, but typically Critical/Major/Moderate are the issues)
        # Let's generate for all to provide complete visibility, but Advisory means "doing okay"

        template = FINDING_TEMPLATES.get(dim_name)
        if template:
            findings.append({
                "type": "dimension",
                "dimension": dim_name,
                "title": template["title"],
                "severity": severity,
                "impact": template["impact"],
                "rationale": f"Score {score_100}/100: {template['rationale']}"
            })

    # 2. Compliance Risk Finding
    if scores.get('compliance_risk_flag'):
        reasons = scores.get('compliance_risk_reasons', [])
        rationale = COMPLIANCE_FINDING["rationale"]
        if reasons:
            rationale += f" Specifically triggered by: {', '.join(reasons)}"

        findings.append({
            "type": "compliance",
            "title": COMPLIANCE_FINDING["title"],
            "severity": COMPLIANCE_FINDING["severity"],
            "impact": COMPLIANCE_FINDING["impact"],
            "rationale": rationale
        })

    # 3. Contradictions Finding
    contradictions = scores.get('contradictions', [])
    if contradictions:
        rationale = CONTRADICTION_FINDING["rationale"]
        rationale += f" {len(contradictions)} contradiction(s) found."

        findings.append({
            "type": "contradiction",
            "title": CONTRADICTION_FINDING["title"],
            "severity": CONTRADICTION_FINDING["severity"],
            "impact": CONTRADICTION_FINDING["impact"],
            "rationale": rationale
        })

    # 4. Missing Data Finding
    missing_data = scores.get('missing_data_flags', [])
    if missing_data:
        rationale = MISSING_DATA_FINDING["rationale"]
        rationale += f" Missing data in: {', '.join(missing_data)}."

        findings.append({
            "type": "missing_data",
            "title": MISSING_DATA_FINDING["title"],
            "severity": MISSING_DATA_FINDING["severity"],
            "impact": MISSING_DATA_FINDING["impact"],
            "rationale": rationale
        })

    return findings

def generate_recommendations(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Maps generated findings to prioritized recommendations.
    """
    recommendations = []

    for finding in findings:
        if finding["type"] == "dimension":
            dim_name = finding["dimension"]
            template = RECOMMENDATION_TEMPLATES.get(dim_name)
            if template:
                severity = finding["severity"]
                impact = DIMENSION_IMPACT.get(dim_name, "Medium")
                priority = determine_priority(severity, impact)

                effort = DIMENSION_EFFORT.get(dim_name, "Medium")

                recommendations.append({
                    "recommendation": template["recommendation"],
                    "priority": priority,
                    "expected_impact": impact,
                    "implementation_effort": effort,
                    "linked_finding": finding["title"]
                })

        elif finding["type"] == "compliance":
            # Priority for compliance is always Immediate since severity is Critical and Impact is High
            recommendations.append({
                "recommendation": COMPLIANCE_FINDING["recommendation"]["recommendation"],
                "priority": "Immediate",
                "expected_impact": COMPLIANCE_FINDING["recommendation"]["expected_impact"],
                "implementation_effort": COMPLIANCE_FINDING["recommendation"]["implementation_effort"],
                "linked_finding": finding["title"]
            })

        elif finding["type"] == "contradiction":
            recommendations.append({
                "recommendation": CONTRADICTION_FINDING["recommendation"]["recommendation"],
                "priority": "Near-Term", # Derived from Major + High Impact conceptually
                "expected_impact": CONTRADICTION_FINDING["recommendation"]["expected_impact"],
                "implementation_effort": CONTRADICTION_FINDING["recommendation"]["implementation_effort"],
                "linked_finding": finding["title"]
            })

        elif finding["type"] == "missing_data":
            recommendations.append({
                "recommendation": MISSING_DATA_FINDING["recommendation"]["recommendation"],
                "priority": "Long-Term", # Derived from Advisory
                "expected_impact": MISSING_DATA_FINDING["recommendation"]["expected_impact"],
                "implementation_effort": MISSING_DATA_FINDING["recommendation"]["implementation_effort"],
                "linked_finding": finding["title"]
            })

    # Deduplicate and sort recommendations by priority? (Immediate -> Near-Term -> Long-Term)
    priority_order = {"Immediate": 1, "Near-Term": 2, "Long-Term": 3}
    recommendations.sort(key=lambda r: priority_order.get(r["priority"], 99))

    return recommendations

def generate_executive_summary(scores: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Generates an executive summary based on assessment scores and generated recommendations.
    """
    summary = {}

    # 1. Overall Assessment
    total_score = sum(scores.get('dimensions', {}).values())
    if total_score >= 80:
        maturity = "High Maturity"
        business_context = "demonstrates advanced AI capabilities with strong alignment across operations."
    elif total_score >= 60:
        maturity = "Moderate Maturity"
        business_context = "shows solid foundational AI adoption, though scaling requires addressing structural gaps."
    elif total_score >= 40:
        maturity = "Developing Capability"
        business_context = "exhibits initial AI usage but lacks the consistency needed for systemic impact."
    else:
        maturity = "Early Stage Capability"
        business_context = "is in the preliminary phases of AI exploration with significant operational vulnerabilities."

    assessment_text = f"The organization {business_context}"
    confidence_index = scores.get('confidence_index', 100)
    if confidence_index < 70:
        assessment_text += " Assessment confidence is reduced due to incomplete or contradictory evidence."

    summary["overall_assessment"] = f"{maturity}. {assessment_text}"

    # 2. Critical Risk
    critical_risk_text = ""
    if scores.get('compliance_risk_flag'):
        critical_risk_text = "Regulatory and compliance exposure is the most immediate threat, requiring urgent legal review of current AI tool usage."
    else:
        # Check for critically low governance score
        gov_score = scores.get('dimensions', {}).get('governance', 0) * 5
        if gov_score <= 39:
            critical_risk_text = "A critical lack of formal AI governance exposes the organization to unmanaged shadow AI and operational risk."
        else:
            # Lowest dimension
            dimensions = scores.get('dimensions', {})
            if dimensions:
                lowest_dim = min(dimensions, key=dimensions.get)
                if lowest_dim == 'integration':
                    critical_risk_text = "System integration bottlenecks present the most significant risk to scaling automation and realizing ROI."
                elif lowest_dim == 'adoption':
                    critical_risk_text = "Fragmented and informal AI adoption patterns threaten operational consistency and increase shadow IT risks."
                elif lowest_dim == 'roi':
                    critical_risk_text = "The inability to measure AI value creation prevents strategic investment and limits organizational buy-in."
                elif lowest_dim == 'awareness':
                    critical_risk_text = "Knowledge silos regarding AI capabilities restrict usage to specific groups, limiting enterprise-wide impact."
                else:
                    critical_risk_text = f"Weaknesses in {lowest_dim} represent the primary operational vulnerability."
            elif scores.get('contradictions'):
                 critical_risk_text = "Operational contradictions indicate a significant gap between stated policies and actual execution."
            else:
                 critical_risk_text = "No critical risks identified based on the provided assessment data."

    summary["critical_risk"] = critical_risk_text

    # 3. Primary Opportunity
    # Leverage order: Governance, Integration, Adoption, ROI, Awareness
    leverage_order = ['governance', 'integration', 'adoption', 'roi', 'awareness']
    dimensions = scores.get('dimensions', {})

    # Identify dimensions that need improvement (e.g., score < 14/20 which is < 70/100)
    improvement_areas = [dim for dim, score in dimensions.items() if score * 5 < 70]

    primary_opportunity = ""
    for dim in leverage_order:
        if dim in improvement_areas:
            if dim == 'governance':
                primary_opportunity = "Formalizing AI adoption governance will structurally improve consistency and risk management across all other initiatives."
            elif dim == 'integration':
                primary_opportunity = "Addressing core system integration readiness will unblock scalable automation and improve data flow."
            elif dim == 'adoption':
                primary_opportunity = "Standardizing localized AI usage into formal playbooks will drive consistent productivity gains."
            elif dim == 'roi':
                primary_opportunity = "Establishing standardized measurement frameworks will immediately improve the ability to justify and focus future AI investments."
            elif dim == 'awareness':
                primary_opportunity = "Launching an enterprise-wide AI literacy program will unlock currently underutilized capabilities and reduce resistance."
            break

    if not primary_opportunity:
        # Fallback if no areas need improvement (highly unlikely, but possible)
        primary_opportunity = "The organization should focus on continuous optimization and extending its advanced capabilities into new strategic areas."

    summary["primary_opportunity"] = primary_opportunity

    # 4. Recommended First Action
    # Select the highest-priority recommendation
    first_action = "Conduct a detailed operational review to determine the next strategic step."
    if recommendations:
        # Since recommendations are already sorted Immediate -> Near-Term -> Long-Term
        first_action = recommendations[0]["recommendation"]

    summary["recommended_first_action"] = first_action

    return summary

def generate_intelligence(scores: Dict[str, Any], industry_type: str | None = None) -> Dict[str, Any]:
    """
    Entrypoint for intelligence generation.
    Takes a raw scores dictionary and returns a structure with findings, recommendations, executive summary,
    target state, roadmap, and dashboard payload.
    """
    findings = generate_findings(scores)
    recommendations = generate_recommendations(findings)
    executive_summary = generate_executive_summary(scores, recommendations)

    # Adapt using Industry Intelligence Engine
    findings = adapt_findings(findings, industry_type)
    recommendations = adapt_recommendations(recommendations, industry_type)
    executive_summary = adapt_executive_summary(executive_summary, industry_type)

    # Clean up internal 'type' and 'dimension' fields from findings before returning
    clean_findings = []
    for f in findings:
        cf = {
            "title": f["title"],
            "severity": f["severity"],
            "impact": f["impact"],
            "rationale": f["rationale"]
        }
        clean_findings.append(cf)

    # Also clean up 'linked_finding' if desired, but might be useful to keep for COI mapping
    clean_recommendations = []
    for r in recommendations:
        cr = {
            "recommendation": r["recommendation"],
            "priority": r["priority"],
            "expected_impact": r["expected_impact"],
            "implementation_effort": r["implementation_effort"],
            "linked_finding": r.get("linked_finding")
        }
        clean_recommendations.append(cr)

    # Generate Target State
    target_state = generate_target_state(scores)

    # Generate Roadmap
    total_score = sum(scores.get('dimensions', {}).values())

    # Generate roadmap requires scaled up dimensions (out of 100) or original
    raw_dimensions = scores.get('dimensions', {})
    scaled_dimensions = {k: v * 5 for k, v in raw_dimensions.items()}

    severity_levels = {f["title"]: f["severity"] for f in clean_findings}

    roadmap_result = generate_roadmap(
        total_score=total_score * 5,
        dimension_scores=scaled_dimensions,
        findings=clean_findings,
        recommendations=clean_recommendations,
        severity_levels=severity_levels
    )

    roadmap = roadmap_result.get("roadmap", {})

    # Generate Dashboard Payload
    dashboard = {
        "critical_risk": executive_summary.get("critical_risk", ""),
        "priority_action": executive_summary.get("recommended_first_action", ""),
        "improvement_opportunity": executive_summary.get("primary_opportunity", ""),
        "executive_summary": executive_summary.get("overall_assessment", "")
    }

    # Generate Failure Intelligence
    failure_intelligence = detect_failure_patterns(scores)

    # Generate Dashboard Payload
    top_failure_risk = None
    if failure_intelligence:
        top_risk = failure_intelligence[0]
        top_failure_risk = {
            "pattern": top_risk["pattern"],
            "severity": top_risk["severity"],
            "recommended_intervention": top_risk["recommended_actions"][0]["intervention"] if top_risk["recommended_actions"] else "Conduct a detailed operational review."
        }

    dashboard = {
        "critical_risk": executive_summary.get("critical_risk", ""),
        "priority_action": executive_summary.get("recommended_first_action", ""),
        "improvement_opportunity": executive_summary.get("primary_opportunity", ""),
        "executive_summary": executive_summary.get("overall_assessment", ""),
        "top_failure_risk": top_failure_risk
    }

    # Generate Risk Projection
    risk_projection = generate_risk_projection(scores, clean_findings)
    risk_projection = adapt_risk_projection(risk_projection, industry_type)

    # Generate Cost of Inaction
    contradiction_count = len(scores.get('contradictions', []))
    confidence_index = scores.get('confidence_index', 100)
    coi = generate_cost_of_inaction(
        findings=findings, # pass original findings so we have access to "type" / "dimension" if needed, though title is used in coi_engine
        recommendations=clean_recommendations,
        dimension_scores=scaled_dimensions,
        contradiction_count=contradiction_count,
        confidence_index=confidence_index
    )

    # Remove 'linked_finding' from recommendations before final output
    for r in clean_recommendations:
        r.pop("linked_finding", None)

    return {
        "executive_summary": executive_summary,
        "findings": clean_findings,
        "recommendations": clean_recommendations,
        "target_state": target_state,
        "roadmap": roadmap,
        "dashboard": dashboard,
        "risk_projection": risk_projection,
        "cost_of_inaction": coi,
        "failure_intelligence": failure_intelligence
    }
