from typing import Dict, Any, List
from backend.prompt_intelligence.llm_service import LLMService

class PromptRewriteEngine:
    """
    Prompt Rewrite Engine to generate improved, operationally deployable prompts.
    It relies entirely on an injected LLMService.
    """

    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    async def rewrite(self, original_prompt: str, context: str, diagnosis: Dict[str, Any], risks: List[str]) -> Dict[str, Any]:

        system_prompt = (
            "You are a Senior Prompt Systems Engineer. Your goal is to rewrite the user's prompt "
            "to make it operationally deployable. The rewritten prompt MUST include: Objective, "
            "Context, Output Expectations, and Success Criteria. Ensure you mitigate the identified risks."
        )

        user_prompt_content = f"""
Original Prompt: {original_prompt}
Detected Context: {context}
Missing Elements: {', '.join(diagnosis.get('missing_elements', []))}
Risks to Mitigate: {', '.join(risks)}
        """

        improved_prompt_string = await self.llm_service.generate(system_prompt, user_prompt_content)

        return {
            "improved_prompt": improved_prompt_string,
            "context": context,
            "rewrite_version": 1
        }
