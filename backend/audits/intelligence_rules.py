from typing import Dict, Any, Tuple

# Severity Thresholds (Score out of 100)
# Note: Raw dimension scores are out of 20, they must be scaled by 5 to out of 100 for these rules.
SEVERITY_THRESHOLDS = {
    "Critical": (0, 39),
    "Major": (40, 54),
    "Moderate": (55, 69),
    "Advisory": (70, 100),
}

# Dimension Business Impact Mapping
DIMENSION_IMPACT = {
    "governance": "High",
    "integration": "High",
    "roi": "Medium-High",
    "adoption": "Medium",
    "awareness": "Medium",
}

# Priority Mapping Logic: (Severity, Business Impact) -> Priority
PRIORITY_MAPPING = {
    ("Critical", "High"): "Immediate",
    ("Critical", "Medium-High"): "Immediate",
    ("Critical", "Medium"): "Immediate",

    ("Major", "High"): "Immediate",
    ("Major", "Medium-High"): "Near-Term",
    ("Major", "Medium"): "Near-Term",

    ("Moderate", "High"): "Near-Term",
    ("Moderate", "Medium-High"): "Near-Term",
    ("Moderate", "Medium"): "Long-Term",

    ("Advisory", "High"): "Long-Term",
    ("Advisory", "Medium-High"): "Long-Term",
    ("Advisory", "Medium"): "Long-Term",
}

# Implementation Effort defaults by Dimension
DIMENSION_EFFORT = {
    "governance": "High",
    "integration": "High",
    "roi": "Medium",
    "adoption": "Medium",
    "awareness": "Low",
}

def determine_severity(score_100: int) -> str:
    for severity, (low, high) in SEVERITY_THRESHOLDS.items():
        if low <= score_100 <= high:
            return severity
    return "Advisory" # Fallback

def determine_priority(severity: str, impact: str) -> str:
    return PRIORITY_MAPPING.get((severity, impact), "Long-Term")


# Content Templates for Findings and Recommendations
FINDING_TEMPLATES = {
    "governance": {
        "title": "AI Governance Framework Vulnerability",
        "impact": "Increased compliance exposure, legal risk, and unmanaged shadow AI.",
        "rationale": "Governance structure is inadequate for the current or target operational scale."
    },
    "integration": {
        "title": "Systems Integration Bottleneck",
        "impact": "Inability to scale automation, resulting in manual data entry and workflow friction.",
        "rationale": "Core software lacks the structural readiness for deep AI integration."
    },
    "roi": {
        "title": "Measurement & Value Tracking Gap",
        "impact": "Inability to justify AI investments or track actual productivity gains.",
        "rationale": "Formal measurement of operational and financial impact is missing."
    },
    "adoption": {
        "title": "Localized & Informal AI Adoption",
        "impact": "Uneven productivity gains and fragmented operational execution.",
        "rationale": "Usage remains localized without systemic integration into daily workflows."
    },
    "awareness": {
        "title": "Organizational Knowledge Silos",
        "impact": "Resistance to change and underutilization of deployed capabilities.",
        "rationale": "General understanding of AI capabilities is restricted to specific groups."
    }
}

RECOMMENDATION_TEMPLATES = {
    "governance": {
        "recommendation": "Establish a formal AI Governance Committee to oversee policy, compliance, and tool approval.",
    },
    "integration": {
        "recommendation": "Execute a workflow diagnostic to map process bottlenecks and prepare core systems for API integrations.",
    },
    "roi": {
        "recommendation": "Implement standardized baseline metrics and tracking mechanisms for all AI initiatives.",
    },
    "adoption": {
        "recommendation": "Develop formal playbooks and standardize AI tool usage across key departments.",
    },
    "awareness": {
        "recommendation": "Launch an organization-wide AI literacy program to align leadership, management, and employees.",
    }
}

# Specific rules for special findings
COMPLIANCE_FINDING = {
    "title": "Regulatory & Compliance Exposure",
    "severity": "Critical",
    "impact": "Direct regulatory vulnerability and potential legal liability.",
    "rationale": "Specific compliance risks identified in responses.",
    "recommendation": {
        "recommendation": "Conduct an immediate legal and compliance review of current AI tool usage.",
        "expected_impact": "High",
        "implementation_effort": "Medium"
    }
}

CONTRADICTION_FINDING = {
    "title": "Operational Contradictions Detected",
    "severity": "Major",
    "impact": "Misalignment between stated capabilities and operational reality.",
    "rationale": "Diagnostic detected conflicting evidence between policy and adoption.",
    "recommendation": {
        "recommendation": "Validate diagnostic findings through direct operational reviews.",
        "expected_impact": "High",
        "implementation_effort": "Low"
    }
}

MISSING_DATA_FINDING = {
    "title": "Structural Visibility Gaps",
    "severity": "Advisory",
    "impact": "Incomplete operational picture preventing full strategic planning.",
    "rationale": "Critical evidence or responses missing from key assessment dimensions.",
    "recommendation": {
        "recommendation": "Mandate complete data collection for subsequent diagnostic iterations.",
        "expected_impact": "Medium",
        "implementation_effort": "Low"
    }
}
