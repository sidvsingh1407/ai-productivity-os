from typing import Dict, Any

class PromptIntelligenceScore:
    """
    Deterministic Intelligence Scoring Engine for quantifying prompt quality.
    Scores range from 0 to 100 based on Clarity, Structure, Output Requirements,
    Operational Usability, Exception Handling, and Decision Criteria.
    """

    @staticmethod
    def evaluate(prompt: str) -> int:
        score = 0
        prompt_lower = prompt.lower()

        # 1. Clarity (0-16)
        clarity_keywords = ["objective:", "goal", "purpose", "aim", "to effectively execute", "context:"]
        clarity_score = sum(8 for kw in clarity_keywords if kw in prompt_lower)
        score += min(16, clarity_score)

        # 2. Structure (0-16)
        structure_keywords = ["section", "step 1", "step 2", "first", "then", "finally", "format:"]
        structure_score = sum(8 for kw in structure_keywords if kw in prompt_lower)
        score += min(16, structure_score)

        # 3. Output Requirements (0-17)
        output_keywords = ["output expectations:", "output format:", "deliverable", "report format", "json format", "markdown"]
        output_score = sum(8 for kw in output_keywords if kw in prompt_lower)
        score += min(17, output_score)

        # 4. Operational Usability (0-17)
        operational_keywords = ["findings", "recommendations", "actionable steps", "owners", "business impact", "dependencies", "tasks:"]
        op_score = sum(8 for kw in operational_keywords if kw in prompt_lower)
        score += min(17, op_score)

        # 5. Exception Handling (0-17)
        exception_keywords = ["fallback", "if missing", "if error", "escalation", "exception", "if unclear"]
        exception_score = sum(8 for kw in exception_keywords if kw in prompt_lower)
        score += min(17, exception_score)

        # 6. Decision Criteria (0-17)
        decision_keywords = ["criteria", "trade-offs", "success criteria", "if", "evaluate", "threshold", "rule"]
        decision_score = sum(8 for kw in decision_keywords if kw in prompt_lower)
        score += min(17, decision_score)

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
