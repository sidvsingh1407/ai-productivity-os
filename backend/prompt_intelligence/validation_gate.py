from typing import Dict, Any, List

class ValidationGate:
    """
    Validation Gate to verify prompt quality before returning results.
    Checks context validity, structural components, operational indicators,
    and risk mitigation based on deterministic rules.
    """

    ALLOWED_CONTEXTS = [
        "Process Automation",
        "Reporting and Analytics",
        "Decision Support",
        "Governance & Compliance",
        "Governance and Compliance",
        "Client Diagnostics",
        "Workflow Design",
        "General Operations"
    ]

    @staticmethod
    def validate(improved_prompt: str, context: str, risks: List[str]) -> Dict[str, Any]:
        errors = []
        prompt_lower = improved_prompt.lower()

        # 1. Context Validation
        if context not in ValidationGate.ALLOWED_CONTEXTS:
            errors.append(f"Invalid context: '{context}'. Must be one of allowed contexts.")

        # 2. Structure Validation
        structural_missing = []
        if "objective" not in prompt_lower:
            structural_missing.append("objective")
        if "context" not in prompt_lower:
            structural_missing.append("context")
        if "output expectations" not in prompt_lower and "output format" not in prompt_lower:
            structural_missing.append("output expectations")

        if structural_missing:
            errors.append(f"Missing required structural elements: {', '.join(structural_missing)}.")

        # 3. Operational Validation
        operational_indicators = ["findings", "recommendations", "actions", "steps", "owners", "priorities", "escalation", "tasks:", "metrics", "dependencies"]
        has_operational = any(indicator in prompt_lower for indicator in operational_indicators)
        if not has_operational:
            errors.append("Prompt lacks operational indicators (e.g., findings, steps, owners).")

        if "think deeply and provide detailed insights" in prompt_lower:
            errors.append("Prompt contains non-operational AI fluff.")

        # 4. Risk Validation (basic deterministic check)
        # In a real app, mapping 'Original Risk' to specific phrases is complex.
        # Here we do simple keyword checks if specific risks were passed.
        for risk in risks:
            risk_lower = risk.lower()
            if "output format" in risk_lower or "ambiguous output" in risk_lower:
                if "output expectations" not in prompt_lower and "output format" not in prompt_lower and "json format" not in prompt_lower and "report format" not in prompt_lower:
                    errors.append(f"Risk not mitigated: '{risk}'. Output format is still missing.")

            if "lack of clear purpose" in risk_lower or "no objective" in risk_lower:
                if "objective:" not in prompt_lower:
                    errors.append(f"Risk not mitigated: '{risk}'. Objective is still unclear.")

        return {
            "passed": len(errors) == 0,
            "errors": errors
        }
