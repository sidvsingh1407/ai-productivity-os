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

def generate_intelligence(scores: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entrypoint for intelligence generation.
    Takes a raw scores dictionary and returns a structure with findings and recommendations.
    """
    findings = generate_findings(scores)
    recommendations = generate_recommendations(findings)

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

    # Also clean up 'linked_finding' if desired, but might be useful to keep
    clean_recommendations = []
    for r in recommendations:
        cr = {
            "recommendation": r["recommendation"],
            "priority": r["priority"],
            "expected_impact": r["expected_impact"],
            "implementation_effort": r["implementation_effort"]
        }
        clean_recommendations.append(cr)

    return {
        "findings": clean_findings,
        "recommendations": clean_recommendations
    }
