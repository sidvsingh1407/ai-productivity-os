import re

with open('docs/research/TARKAX_CONFIDENCE_INDEX_V1.md', 'r') as f:
    content = f.read()

# Add "Factors that do NOT influence confidence"
factors_not_influence = """### Factors that do NOT influence confidence
*   **Organizational Health/Capability Score:** A company with "Fragile" capabilities can still have a 100% Confidence Index if they provided perfect evidence of their fragility.
*   **Assessment Speed:** How fast the user completed the assessment.
*   **Company Revenue or Size (Directly):** While demographic alignment matters for benchmarking, raw size does not dictate truthfulness.

"""
content = re.sub(r'(## Confidence Index Dimensions\n\nThe Confidence Index is 100% deterministic, utilizing a weighted rules engine. It is never directly calculated by an LLM.\n\n)', r'\1' + factors_not_influence, content)


# Add Output Examples section
output_examples = """## Output Examples

### Example 1: High Confidence
**AI Maturity:** Operational
**Confidence:** 82% (Very High Confidence)
**Reason:**
✓ Assessment completed
✓ Evidence provided
✓ No major contradictions
✓ Benchmark coverage available

### Example 2: Low Confidence
**Workflow Health:** 63
**Confidence:** 41% (Moderate Confidence)
**Reason:**
✗ Missing evidence
✗ Incomplete responses
✗ Contradictions detected

"""
content = re.sub(r'(## Report Integration & Influence Logic\n\n)', output_examples + r'\1', content)


# Update Report Integration specific sections
report_integration = """## Report Integration & Influence Logic

The Confidence Index is not merely a display metric; it is an operational governor. It actively alters the behavior, tone, and scope of specific TarkaX reports.

### Specific Audit Integrations

1.  **AI Audit:** If confidence is low due to lack of technical evidence (e.g., missing API specs), the report will restrict recommendations for custom LLM deployments and default to off-the-shelf suggestions, flagging the need for deeper technical verification.
2.  **Workflow Diagnostic:** Low confidence (often due to missing process owners or missing workflow maps) will prevent the simulation engine from generating aggressive cost-saving forecasts, instead outputting a recommendation to "Define current state workflow."
3.  **Leadership Audit:** Highly sensitive to "Contradiction Risk" (e.g., Leaders claim high alignment, but lower-level data contradicts). If the Confidence Index drops due to internal inconsistency, the report shifts from "Strategic Execution" to "Alignment Discovery."
4.  **Manager Audit:** Confidence hinges on L3/L4 evidence (Tool Context, Process Ownership). Low confidence restricts operational KPI forecasting.
5.  **Employee Audit:** Often relies on high-volume, lower-tier evidence (L1/L2). Confidence index scales based on participation rates. Low confidence triggers recommendations for "Broader organizational sampling."
6.  **Organizational Alignment Audit:** The ultimate aggregator. The Confidence Index here is a meta-score derived from the variance between Leadership, Manager, and Employee audits. High variance severely penalizes the Confidence Index, altering the report to focus strictly on resolving communication gaps rather than APQC optimizations.

### General Influence Logic Based on Thresholds
"""

content = re.sub(r'(## Report Integration & Influence Logic\n\nThe Confidence Index is not merely a display metric; it is an operational governor. It actively alters the behavior, tone, and scope of TarkaX reports \(AI Audits, Workflow Diagnostics, Leadership Audits\).\n\n)', report_integration, content)

with open('docs/research/TARKAX_CONFIDENCE_INDEX_V1.md', 'w') as f:
    f.write(content)
