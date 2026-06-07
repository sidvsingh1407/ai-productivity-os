import re
from typing import Dict, Any, List
from prompt_intelligence.diagnosis_rules import (
    ELEMENT_RULES,
    ELEMENT_PENALTIES,
    STRENGTH_THRESHOLDS,
    EXECUTION_RISKS_MAPPING
)

class DiagnosisEngine:
    """
    Deterministic engine for evaluating prompt strength, identifying missing elements,
    and calculating execution risks.
    """

    @staticmethod
    def _determine_strength(score: int) -> str:
        for strength, (min_score, max_score) in STRENGTH_THRESHOLDS.items():
            if min_score <= score <= max_score:
                return strength
        return "Broken" # Fallback if below 0

    @staticmethod
    def diagnose(prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()

        score = 100
        missing_elements = []
        execution_risks = []

        for element_type, keywords in ELEMENT_RULES.items():
            element_found = False
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, prompt_lower):
                    element_found = True
                    break

            if not element_found:
                missing_elements.append(element_type)
                score -= ELEMENT_PENALTIES.get(element_type, 0)

                # Add corresponding risk
                if element_type in EXECUTION_RISKS_MAPPING:
                    risk = EXECUTION_RISKS_MAPPING[element_type]
                    if risk not in execution_risks:
                        execution_risks.append(risk)

        # Ensure score does not drop below 0
        score = max(0, score)

        strength = DiagnosisEngine._determine_strength(score)

        return {
            "strength": strength,
            "missing_elements": missing_elements,
            "execution_risks": execution_risks
        }
