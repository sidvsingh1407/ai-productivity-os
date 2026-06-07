from typing import Dict, Any, List
from backend.prompt_intelligence.context_classifier import ContextClassifier
from backend.prompt_intelligence.diagnosis_engine import DiagnosisEngine
from backend.prompt_intelligence.prompt_rewrite_engine import PromptRewriteEngine
from backend.prompt_intelligence.llm_service import LLMService

class PromptIntelligenceService:
    def __init__(self):
        self.rewrite_engine = PromptRewriteEngine(llm_service=LLMService())

    async def process_prompt(self, prompt: str) -> Dict[str, Any]:
        # 1. Context Detection
        context_result = ContextClassifier.classify(prompt)
        category = context_result.get("context", "Unclassified")
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

        # Assemble the final response exactly matching output model
        response = {
            "context": category,
            "environment": environment,
            "strength": strength,
            "missing_elements": missing_elements,
            "execution_risks": execution_risks,
            "improved_prompt": improved_prompt,
            "improvement_rationale": improvement_rationale
        }

        return response
