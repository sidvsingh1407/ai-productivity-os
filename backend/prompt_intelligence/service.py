from typing import Dict, Any, List
from prompt_intelligence.context_classifier import ContextClassifier
from prompt_intelligence.diagnosis_engine import DiagnosisEngine
from prompt_intelligence.prompt_rewrite_engine import PromptRewriteEngine
from prompt_intelligence.validation_gate import ValidationGate
from prompt_intelligence.prompt_intelligence_score import PromptIntelligenceScore
from prompt_intelligence.llm_service import LLMService

class PromptIntelligenceService:
    def __init__(self):
        self.rewrite_engine = PromptRewriteEngine(llm_service=LLMService())

    async def process_prompt(self, prompt: str) -> Dict[str, Any]:
        # 1. Context Detection
        context_result = ContextClassifier.classify(prompt)
        category = context_result.get("context", "Unclassified")
        confidence = context_result.get("confidence", 0.0)

        # 2. Diagnosis
        diagnosis_result = DiagnosisEngine.diagnose(prompt)
        missing_elements = diagnosis_result.get("missing_elements", [])
        execution_risks = diagnosis_result.get("execution_risks", [])
        strength = diagnosis_result.get("strength", "Weak")

        # 3. Prompt Rewrite
        rewrite_result = await self.rewrite_engine.rewrite(
            original_prompt=prompt,
            context=category,
            diagnosis=diagnosis_result,
            risks=execution_risks
        )
        improved_prompt = rewrite_result.get("improved_prompt", "")

        # 4. Validation
        validation_result = ValidationGate.validate(
            improved_prompt=improved_prompt,
            context=category,
            risks=execution_risks
        )

        # 5. Scoring
        scores = PromptIntelligenceScore.compare(
            original_prompt=prompt,
            improved_prompt=improved_prompt
        )

        # Determine rationales based on diagnosis and risks
        changes_made = []
        if missing_elements:
            changes_made.append(f"Added structural elements: {', '.join(missing_elements)}")
        changes_made.append("Optimized instructions for clarity and objective focus.")

        failure_modes_addressed = execution_risks

        # Assemble the final response
        response = {
            "context": {
                "category": category,
                "confidence": confidence
            },
            "diagnosis": {
                "strength": strength,
                "missing": missing_elements,
                "execution_risks": execution_risks
            },
            "scores": {
                "original_score": scores.get("original_score", 0),
                "improved_score": scores.get("improved_score", 0)
            },
            "validation": {
                "passed": validation_result.get("passed", False),
                "errors": validation_result.get("errors", [])
            },
            "improved_prompt": improved_prompt,
            "rationale": {
                "changes_made": changes_made,
                "failure_modes_addressed": failure_modes_addressed
            }
        }

        return response
