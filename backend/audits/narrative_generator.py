import json
import logging
from typing import Dict, Any, Optional

from utils.gemini_client import get_gemini_response

logger = logging.getLogger(__name__)

def generate_audit_narrative(
    company_context: Dict[str, Any],
    scores: Dict[str, Any],
    risk_findings: Dict[str, Any],
    roadmap: Dict[str, Any],
    coi: Any,
    target_state: Any
) -> Optional[Dict[str, Any]]:
    """
    Generates a dynamic narrative for the AI Audit using Gemini.
    Returns the parsed JSON dictionary if successful, or None if it fails.
    """

    industry = company_context.get("industry", "Not specified")
    company_size = company_context.get("company_size", "Not specified")
    region = company_context.get("region", "Not specified")
    ai_usage_description = company_context.get("ai_usage", "Not specified")
    governance_level = company_context.get("governance_level", "Not specified")

    overall_score = scores.get("total_score", "N/A")
    dimensions = scores.get("dimensions", {})
    awareness_score = dimensions.get("awareness", 0) * 5
    adoption_score = dimensions.get("adoption", 0) * 5
    integration_score = dimensions.get("integration", 0) * 5
    governance_score = dimensions.get("governance", 0) * 5
    roi_score = dimensions.get("roi", 0) * 5

    try:
        risk_findings_json = json.dumps(risk_findings, indent=2)
    except Exception:
        risk_findings_json = str(risk_findings)

    try:
        roadmap_json = json.dumps(roadmap, indent=2)
    except Exception:
        roadmap_json = str(roadmap)

    try:
        coi_json = json.dumps(coi, indent=2)
    except Exception:
        coi_json = str(coi)

    prompt = f"""You are a senior AI governance consultant writing an executive audit report.

COMPANY PROFILE:
- Industry: {industry}
- Company size: {company_size} employees
- Region: {region}
- Current AI usage: {ai_usage_description}
- Governance maturity: {governance_level}

AUDIT SCORES (calculated by our scoring engine):
- Overall AI Maturity Score: {overall_score}/100
- Awareness: {awareness_score}/100
- Adoption: {adoption_score}/100
- Integration: {integration_score}/100
- Governance: {governance_score}/100
- ROI: {roi_score}/100

RISK FINDINGS:
{risk_findings_json}

30/60/90 DAY ROADMAP:
{roadmap_json}

COST OF INACTION ANALYSIS:
{coi_json}

Write a professional executive audit narrative that:
1. Opens with a 2-3 sentence executive summary that directly references this company's specific profile, size, industry, and region
2. Identifies the 2-3 most critical findings based on the lowest dimension scores, explained in business terms (not technical jargon)
3. Calls out the single highest-priority action this specific company must take first, and why
4. References EU AI Act compliance exposure if the company operates in Europe
5. Closes with the cost of inaction framed in business impact terms

Respond ONLY with a valid JSON object in this exact structure:
{{
  "executive_summary": "string",
  "critical_findings": ["string", "string", "string"],
  "highest_priority_action": "string",
  "regulatory_exposure": "string or null",
  "cost_of_inaction_narrative": "string"
}}

Do not include markdown, backticks, or any text outside the JSON object.
"""

    try:
        response_text = get_gemini_response(prompt)
        # Attempt to parse the JSON response
        # Strip potential backticks if the model still includes them despite instructions
        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()

        narrative_json = json.loads(clean_text)
        return narrative_json
    except Exception as e:
        logger.error(f"Failed to generate or parse AI Audit narrative via Gemini: {str(e)}")
        # If parsing fails or API fails, log error and return None
        return None
