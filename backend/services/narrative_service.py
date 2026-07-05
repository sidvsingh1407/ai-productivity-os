import json
import logging
from .gemini_client import gemini_manager

logger = logging.getLogger(__name__)

def _parse_gemini_json(raw: str) -> dict | None:
    """Strip markdown fences and parse JSON defensively."""
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        return json.loads(cleaned.strip())
    except Exception as e:
        logger.error(f"Failed to parse Gemini JSON response: {e}. Raw: {raw[:200]}")
        return None

async def generate_audit_narrative(scores: dict, company_context: dict) -> dict | None:
    prompt = f"""
You are a senior AI governance consultant writing a confidential assessment report.

A company has completed an AI maturity audit. Write a specific, actionable narrative.
Reference their actual company details throughout. Every sentence must feel written for this specific company.
Do not use generic boilerplate that could apply to any company.

COMPANY PROFILE:
- Company name: {company_context.get('company_name', 'the organization')}
- Industry: {company_context.get('industry', 'unspecified')}
- Company size: {company_context.get('company_size', 'unspecified')} employees
- Region: {company_context.get('region', 'unspecified')}
- Current AI usage: {company_context.get('ai_usage_description', 'unspecified')}
- Governance status: {company_context.get('governance_status', 'unspecified')}

AUDIT SCORES (0-100):
- Overall maturity score: {scores.get('overall_score')}
- Awareness: {scores.get('awareness_score')}
- Adoption: {scores.get('adoption_score')}
- Integration: {scores.get('integration_score')}
- Governance: {scores.get('governance_score')}
- ROI: {scores.get('roi_score')}

Respond ONLY with a valid JSON object. No preamble, no markdown, no explanation:
{{
  "executive_summary": {{
    "overall_assessment": "2-3 sentence assessment specific to this company profile and scores",
    "critical_risk": "The single most important risk for this company given their industry and governance score",
    "primary_opportunity": "Highest-leverage opportunity specific to their size and adoption level",
    "recommended_first_action": "Concrete specific first action tailored to their situation"
  }},
  "dimension_narratives": {{
    "awareness": "1-2 sentences on their awareness score in context of their industry",
    "adoption": "1-2 sentences on their adoption score referencing company size",
    "integration": "1-2 sentences on their integration score",
    "governance": "1-2 sentences on governance score referencing region if EU-relevant",
    "roi": "1-2 sentences on their ROI score"
  }},
  "roadmap": {{
    "day_30": "Specific 30-day action tailored to their biggest gap",
    "day_60": "Specific 60-day action building on day 30",
    "day_90": "Specific 90-day action moving toward their primary opportunity"
  }},
  "recommendations": [
    {{
      "recommendation": "Specific recommendation referencing their company context",
      "priority": "Critical | High | Medium",
      "rationale": "Why this matters specifically for their industry, size, and region"
    }}
  ]
}}
"""
    raw = await gemini_manager.generate(prompt)
    if not raw:
        return None
    return _parse_gemini_json(raw)


async def generate_workflow_narrative(scores: dict, workflow_context: dict) -> dict | None:
    prompt = f"""
You are a senior operations consultant writing a confidential workflow diagnostic report.

Write a specific, actionable narrative referencing the company's actual workflow details,
industry, and size throughout. Do not use generic boilerplate.

COMPANY PROFILE:
- Company name: {workflow_context.get('company_name', 'the organization')}
- Industry: {workflow_context.get('industry', 'unspecified')}
- Company size: {workflow_context.get('company_size', 'unspecified')} employees
- Workflow described: {workflow_context.get('workflow_description', 'unspecified')}
- Current automation level: {workflow_context.get('automation_level', 'unspecified')}

DIAGNOSTIC SCORES:
- Overall workflow maturity: {scores.get('workflow_maturity')}
- Automation coverage: {scores.get('automation_score')}
- Friction level: {scores.get('friction_score')}
- AI opportunity score: {scores.get('ai_opportunity_score')}

Respond ONLY with a valid JSON object. No preamble, no markdown, no explanation:
{{
  "executive_summary": {{
    "most_critical_bottleneck": "Specific bottleneck in their described workflow",
    "primary_root_cause": "Root cause specific to their industry and company size",
    "highest_priority_intervention": "Concrete intervention for their specific workflow",
    "workflow_risk_level": "Low | Medium | High | Critical",
    "workflow_maturity": "One-line maturity label specific to their situation"
  }},
  "bottlenecks": [
    {{
      "title": "Specific bottleneck referencing their workflow",
      "severity": "Critical | High | Advisory",
      "impacted_area": "Specific area of their workflow",
      "rationale": "Why this is a bottleneck for a company of their size and industry"
    }}
  ],
  "automation_opportunities": [
    {{
      "process": "Specific process from their workflow description",
      "automation_type": "RPA | AI | Script | Low-code",
      "estimated_time_saving": "Realistic estimate for their company size",
      "implementation_effort": "Low | Medium | High"
    }}
  ],
  "recommendations": [
    {{
      "recommendation": "Specific recommendation for their workflow",
      "priority": "Near-Term | Medium-Term | Strategic",
      "expected_impact": "Concrete impact specific to their industry",
      "implementation_effort": "Low | Medium | High"
    }}
  ]
}}
"""
    raw = await gemini_manager.generate(prompt)
    if not raw:
        return None
    return _parse_gemini_json(raw)
