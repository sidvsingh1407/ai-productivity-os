from typing import Dict, Any, List
import os
import json
from prompt_intelligence.llm_service import LLMService

class PromptRewriteEngine:
    """
    Prompt Rewrite Engine to generate improved, operationally deployable prompts.
    It relies entirely on an injected LLMService.
    """

    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def _load_system_prompt(self) -> str:
        prompt_path = os.path.join(
            os.path.dirname(__file__),
            "system_prompts",
            "business_operations_specialist.txt"
        )
        try:
            with open(prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "System prompt file not found."

    async def rewrite(self, original_prompt: str, context: str, diagnosis: Dict[str, Any], risks: List[str]) -> Dict[str, Any]:

        system_prompt = self._load_system_prompt()

        user_prompt_content = f"""
Original Prompt: {original_prompt}
Detected Context: {context}
Missing Elements: {', '.join(diagnosis.get('missing_elements', []))}
Risks to Mitigate: {', '.join(risks)}
        """

        llm_output = await self.llm_service.generate(system_prompt, user_prompt_content)

        improved_prompt = ""
        improvement_rationale = {}

        # Parse LLM Output for Sections
        if "SECTION 3 — IMPROVED PROMPT" in llm_output and "SECTION 4 — IMPROVEMENT RATIONALE" in llm_output:
            parts = llm_output.split("SECTION 4 — IMPROVEMENT RATIONALE")
            improved_prompt_part = parts[0].split("SECTION 3 — IMPROVED PROMPT")[-1].strip()
            rationale_part = parts[1].strip()

            improved_prompt = improved_prompt_part
            try:
                improvement_rationale = json.loads(rationale_part)
            except json.JSONDecodeError:
                improvement_rationale = {"error": "Failed to parse JSON rationale from LLM output.", "raw": rationale_part}
        else:
             improved_prompt = llm_output
             improvement_rationale = {"error": "Output sections missing."}

        return {
            "improved_prompt": improved_prompt,
            "improvement_rationale": improvement_rationale
        }
