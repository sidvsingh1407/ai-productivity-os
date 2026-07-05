import json
import logging
from typing import Dict, Any, List, Optional

from utils.gemini_client import get_gemini_response

logger = logging.getLogger(__name__)

def generate_workflow_narrative(
    workflow_context: Dict[str, Any],
    intelligence: Dict[str, Any],
    bottlenecks: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Generates a dynamic narrative for the Workflow Diagnostic using Gemini.
    Returns the parsed JSON dictionary if successful, or None if it fails.
    """

    process_name = workflow_context.get("process_name", "Not specified")
    workflow_description = workflow_context.get("description", "Not specified")
    team_size = workflow_context.get("team_size", "Not specified")
    tools_list = workflow_context.get("tools", "Not specified")
    time_estimate = workflow_context.get("time_estimate", "Not specified")

    workflow_maturity = intelligence.get("workflow_maturity", "N/A")
    workflow_risk_level = intelligence.get("workflow_risk_level", "N/A")
    automation_score = intelligence.get("automation_coverage", "N/A")

    try:
        bottlenecks_json = json.dumps(bottlenecks, indent=2)
    except Exception:
        bottlenecks_json = str(bottlenecks)

    try:
        recommendations_json = json.dumps(recommendations, indent=2)
    except Exception:
        recommendations_json = str(recommendations)

    prompt = f"""You are a senior operations consultant writing a workflow diagnostic report.

WORKFLOW SUBMITTED:
- Process name: {process_name}
- Description: {workflow_description}
- Team size involved: {team_size}
- Tools currently used: {tools_list}
- Estimated time per cycle: {time_estimate}

DIAGNOSTIC RESULTS (calculated by our analysis engine):
- Workflow maturity: {workflow_maturity}
- Risk level: {workflow_risk_level}
- Automation coverage score: {automation_score}

IDENTIFIED BOTTLENECKS:
{bottlenecks_json}

RECOMMENDATIONS:
{recommendations_json}

Write a professional workflow diagnostic narrative that:
1. Opens with a summary that specifically names this workflow and its context
2. Explains the most critical bottleneck in plain business language — what it costs the team, not just what it is
3. Identifies the single highest-ROI automation opportunity specific to this workflow
4. Gives one concrete next step the team can take this week
5. Closes with the expected business impact if the top recommendation is implemented

Respond ONLY with a valid JSON object in this exact structure:
{{
  "executive_summary": "string",
  "critical_bottleneck_analysis": "string",
  "top_automation_opportunity": "string",
  "immediate_next_step": "string",
  "expected_impact": "string"
}}

Do not include markdown, backticks, or any text outside the JSON object.
"""

    try:
        response_text = get_gemini_response(prompt)
        # Attempt to parse the JSON response
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
        logger.error(f"Failed to generate or parse Workflow Diagnostic narrative via Gemini: {str(e)}")
        # If parsing fails or API fails, log error and return None
        return None
