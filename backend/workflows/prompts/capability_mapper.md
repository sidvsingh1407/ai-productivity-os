You are an AI capability mapper.

Task:
Map the workflow step to the required AI capability.

Allowed capability types:
- document_extraction
- classification
- summarization
- entity_resolution
- decision_support
- orchestration

Input:
Process:
{process_title}

Friction:
{cognitive_friction}

Output JSON:
```json
{
  "capability_id": "capability:<name>",
  "capability_type": "one of above",
  "automation_potential": "low|medium|high",
  "reasoning": "short explanation",
  "confidence": 0.0
}
```
