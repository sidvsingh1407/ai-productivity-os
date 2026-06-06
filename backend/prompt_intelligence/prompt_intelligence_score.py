from typing import Dict, Any

class PromptIntelligenceScore:
    """
    Deterministic Intelligence Scoring Engine for quantifying prompt quality.
    Scores range from 0 to 100 based on Objective Clarity, Context Completeness,
    Output Definition, Operational Usability, and Risk Mitigation.
    """

    @staticmethod
    def evaluate(prompt: str) -> int:
        score = 0
        prompt_lower = prompt.lower()

        # 1. Objective Clarity (0-20)
        objective_keywords = ["objective:", "goal", "purpose", "aim", "to effectively execute"]
        objective_score = 0
        for kw in objective_keywords:
            if kw in prompt_lower:
                objective_score += 10
        score += min(20, objective_score)

        # 2. Context Completeness (0-20)
        context_keywords = ["context:", "background", "situation", "this task is related to"]
        context_score = 0
        for kw in context_keywords:
            if kw in prompt_lower:
                context_score += 10
        score += min(20, context_score)

        # 3. Output Definition (0-20)
        output_keywords = ["output expectations:", "output format:", "deliverable", "report format", "json format"]
        output_score = 0
        for kw in output_keywords:
            if kw in prompt_lower:
                output_score += 10
        score += min(20, output_score)

        # 4. Operational Usability (0-20)
        operational_keywords = ["findings", "recommendations", "actionable steps", "owners", "business impact", "dependencies", "tasks:"]
        op_score = 0
        for kw in operational_keywords:
            if kw in prompt_lower:
                op_score += 5
        score += min(20, op_score)

        # 5. Risk Mitigation / Constraints / Success Criteria (0-20)
        risk_keywords = ["success criteria:", "constraints", "trade-offs", "risk mitigation", "quality standards"]
        risk_score = 0
        for kw in risk_keywords:
            if kw in prompt_lower:
                risk_score += 10
        score += min(20, risk_score)

        return min(100, score)

    @staticmethod
    def compare(original_prompt: str, improved_prompt: str) -> Dict[str, int]:
        original_score = PromptIntelligenceScore.evaluate(original_prompt)
        improved_score = PromptIntelligenceScore.evaluate(improved_prompt)

        return {
            "original_score": original_score,
            "improved_score": improved_score,
            "improvement_delta": improved_score - original_score
        }
