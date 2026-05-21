You are an enterprise AI workflow architect.

Task:
Generate a deterministic automation blueprint.

Inputs:
Process:
{process_title}

Friction:
{cognitive_friction}

Capability:
{capability_id}

Constraints:
- Max 5 steps
- Each step must include input/output
- HITL must be explicitly defined
- No vague steps

Output JSON:
```json
{
  "blueprint": {
    "title": "string",
    "automation_tier": "full|hitl|augmented",
    "orchestration_pipeline": [
      {
        "step": 1,
        "action": "string",
        "capability_id": "string",
        "input": "string",
        "output": "string",
        "hitl_required": true
      }
    ],
    "hitl_checkpoint": "string|null",
    "estimated_time_saved": "string",
    "confidence": 0.0
  }
}
```
