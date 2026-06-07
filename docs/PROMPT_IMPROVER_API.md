# Prompt Improver API

Internal API for powering the Prompt Improver intelligence engine. This endpoint evaluates a given prompt and returns a structurally sound, operationally deployable improved prompt, along with an operational diagnosis and intelligence scores.

### Endpoint
`POST /api/prompt-improver`

**Authentication:**
Requires standard application JWT via `Authorization: Bearer <token>`.

### Request Example
```json
{
  "prompt": "Build an approval workflow."
}
```

### Response Example
```json
{
  "operational_context": {
    "detected_context": "Process Automation",
    "purpose": "Executing tasks for Process Automation",
    "operational_environment": "Internal Operations"
  },
  "diagnosis": {
    "strength": "Broken",
    "missing_elements": [
      "Context",
      "Constraints",
      "Ownership",
      "Outputs",
      "Escalation Paths"
    ],
    "execution_risks": [
      "Lack of Clear Purpose",
      "Inconsistent Responses",
      "Misaligned Recommendations",
      "Ambiguous Output",
      "Failure During Edge Cases"
    ]
  },
  "improved_prompt": "SECTION 3 — IMPROVED PROMPT\n\nObjective: To effectively execute tasks within Process Automation.\n\nContext: This task is related to Process Automation. Consider standard operational constraints.\n\nTasks: Identify manual steps, design approval workflows, and set up automated triggers.\n\nOutput Expectations: Provide actionable steps, owners, and trigger definitions in JSON format.\n\nSuccess Criteria: The workflow must reduce manual steps by 50%.\n",
  "improvement_rationale": {
    "context_reasoning": "Matched operational keywords to 'Process Automation'.",
    "changes_made": [
      "Added structural elements based on context",
      "Optimized instructions for clarity and objective focus."
    ],
    "failure_modes_addressed": [
      "Addressed Ambiguous Output",
      "Mitigated Execution Failure During Edge Cases"
    ],
    "expected_improvements": "The improved prompt produces a structured, predictable outcome."
  },
  "intelligence_scores": {
    "original_score": 0,
    "improved_score": 58
  },
  "validation": {
    "passed": true,
    "validation_errors": []
  }
}
```

### Error Example
```json
{
  "detail": "Prompt cannot be empty"
}
```

```json
{
  "validation": {
    "passed": false,
    "validation_errors": [
      "Missing required structural elements: objective, context, output expectations."
    ]
  }
}
```
