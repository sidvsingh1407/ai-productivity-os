You are a workflow diagnostic system.

Task:
Identify the primary friction type in this workflow step.

Allowed friction types:
- unstructured_data
- reconciliation
- routing
- decision_ambiguity

Input:
{normalized_text}

Output JSON:
```json
{
  "cognitive_friction": "one of above",
  "friction_severity": "low|medium|high",
  "mechanical_friction": "optional string",
  "hitl_need": "none|validation|decision",
  "confidence": 0.0
}
```
