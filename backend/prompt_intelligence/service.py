from typing import Dict, Any, List
from prompt_intelligence.context_classifier import ContextClassifier
from prompt_intelligence.diagnosis_engine import DiagnosisEngine
from prompt_intelligence.prompt_rewrite_engine import PromptRewriteEngine
from prompt_intelligence.llm_service import LLMService

class PromptIntelligenceService:
    def __init__(self):
        self.rewrite_engine = PromptRewriteEngine(llm_service=LLMService())

    async def process_prompt(self, prompt: str) -> Dict[str, Any]:
        # 1. Context Detection
        context_result = ContextClassifier.classify(prompt)
        category = context_result.get("context", "General Operations")
        environment = context_result.get("environment", "General Business Operations")

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
        improvement_rationale = rewrite_result.get("improvement_rationale", {})

        # 4. Scoring
        from prompt_intelligence.prompt_intelligence_score import PromptIntelligenceScore
        score_comparison = PromptIntelligenceScore.compare(prompt, improved_prompt)
        original_score = score_comparison.get("original_score", 0)
        improved_score = score_comparison.get("improved_score", 0)

        # 5. Validation
        from prompt_intelligence.validation_gate import ValidationGate
        validation_result = ValidationGate.validate(improved_prompt, category, execution_risks)
        validation_passed = validation_result.get("passed", False)
        validation_errors = validation_result.get("errors", [])

        # Assemble the final response exactly matching output model
        response = {
            "operational_context": {
                "detected_context": category,
                "purpose": f"Executing tasks for {category}",
                "operational_environment": environment
            },
            "diagnosis": {
                "strength": strength,
                "missing_elements": missing_elements,
                "execution_risks": execution_risks
            },
            "improved_prompt": improved_prompt,
            "improvement_rationale": improvement_rationale,
            "intelligence_scores": {
                "original_score": original_score,
                "improved_score": improved_score
            },
            "validation": {
                "passed": validation_passed,
                "validation_errors": validation_errors
            }
        }

        return response
