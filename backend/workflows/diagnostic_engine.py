from typing import List, Dict, Any

STRENGTH_THRESHOLD = 80
WEAKNESS_THRESHOLD = 50

def calculate_diagnostic_scores(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_steps = len(steps)
    if total_steps == 0:
        return {
            "scores": {
                "bottleneck": 100,
                "governance": 100,
                "ambiguity": 100,
                "risk": 100,
                "health": 100
            },
            "findings": {
                "strengths": [],
                "weaknesses": [],
                "priority_actions": ["Add steps to diagnose the workflow."]
            }
        }

    manual_handoff_count = 0
    missing_tool_count = 0
    unrecorded_approval_count = 0
    missing_owner_count = 0
    missing_owner_or_tool_count = 0

    owner_counts = {}

    for step in steps:
        manual_handoff = step.get("manual_handoff", False)
        system_tool = step.get("system_tool")
        requires_approval = step.get("requires_approval", False)
        owner_role = step.get("owner_role")

        if manual_handoff:
            manual_handoff_count += 1

        if not system_tool and not manual_handoff:
            missing_tool_count += 1

        if requires_approval and not system_tool:
            unrecorded_approval_count += 1

        if not owner_role:
            missing_owner_count += 1

        if not owner_role or not system_tool:
            missing_owner_or_tool_count += 1

        if owner_role:
            owner_counts[owner_role] = owner_counts.get(owner_role, 0) + 1

    # Normalizing penalties
    # Bottleneck: 100% manual handoffs -> -50, 100% missing tools -> -50.
    bottleneck_penalty = (manual_handoff_count / total_steps) * 50 + (missing_tool_count / total_steps) * 50
    bottleneck_score = max(0, int(100 - bottleneck_penalty))

    # Governance: 100% unrecorded approvals -> -60, 100% missing owners -> -40.
    governance_penalty = (unrecorded_approval_count / total_steps) * 60 + (missing_owner_count / total_steps) * 40
    governance_score = max(0, int(100 - governance_penalty))

    # Ambiguity: Steps with both owner and tool / total steps
    ambiguity_score = int(((total_steps - missing_owner_or_tool_count) / total_steps) * 100)

    # Risk: Bus factor penalty
    max_owner_percentage = 0
    if owner_counts:
        max_owner_percentage = max(owner_counts.values()) / total_steps

    bus_factor_penalty = 0
    if max_owner_percentage > 0.5:
        bus_factor_penalty = (max_owner_percentage - 0.5) * 2 * 50 # If 100%, penalty is 50.

    # Risk: Fragility penalty (manual handoffs)
    fragility_penalty = (manual_handoff_count / total_steps) * 50
    risk_score = max(0, int(100 - bus_factor_penalty - fragility_penalty))

    health_score = int((bottleneck_score + governance_score + ambiguity_score + risk_score) / 4)

    scores = {
        "bottleneck": bottleneck_score,
        "governance": governance_score,
        "ambiguity": ambiguity_score,
        "risk": risk_score,
        "health": health_score
    }

    # Findings logic
    strengths = []
    weaknesses = []
    priority_actions = []

    if governance_score >= STRENGTH_THRESHOLD:
        strengths.append("High governance: Approvals and steps are well-documented in system tools.")
    if ambiguity_score >= STRENGTH_THRESHOLD:
        strengths.append("Clear ownership: Steps have assigned roles and system tools.")
    if bottleneck_score >= STRENGTH_THRESHOLD:
        strengths.append("Efficient execution: Low manual handoffs and consistent tooling.")

    if bottleneck_score < WEAKNESS_THRESHOLD:
        weaknesses.append("Heavy manual handoffs or missing tools introduce significant delays.")
    if governance_score < WEAKNESS_THRESHOLD:
        weaknesses.append("High risk of unrecorded approvals or missing step owners.")
    if risk_score < WEAKNESS_THRESHOLD:
        weaknesses.append("Workflow is fragile due to manual handoffs or a high bus factor.")
    if ambiguity_score < WEAKNESS_THRESHOLD:
        weaknesses.append("Process is ambiguous due to missing owners or system tools.")

    # Find the lowest score to drive priority actions
    lowest_score_key = min(scores, key=scores.get)
    if lowest_score_key == "bottleneck":
        priority_actions.append("Digitize manual handoffs and ensure all non-manual steps have associated system tools.")
    elif lowest_score_key == "governance":
        priority_actions.append("Require a system of record for all approval steps and ensure every step has an owner.")
    elif lowest_score_key == "ambiguity":
        priority_actions.append("Assign specific owner roles and system tools to unowned steps.")
    elif lowest_score_key == "risk":
        priority_actions.append("Distribute step ownership across multiple roles to reduce single points of failure.")
    else:
        priority_actions.append("Review workflow structure for potential efficiency gains.")

    return {
        "scores": scores,
        "findings": {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "priority_actions": priority_actions
        }
    }
