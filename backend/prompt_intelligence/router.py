from fastapi import APIRouter, HTTPException, Response
from prompt_intelligence.schemas import PromptRequest, PromptResponse, ValidationFailureResponse
from prompt_intelligence.service import PromptIntelligenceService
from typing import Union

router = APIRouter(tags=["Prompt Intelligence"])
service = PromptIntelligenceService()

@router.post("/prompt-improver", response_model=Union[PromptResponse, ValidationFailureResponse])
async def prompt_improver(request: PromptRequest):
    prompt_text = request.prompt.strip()

    if not prompt_text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    if len(prompt_text) > 10000:
        raise HTTPException(status_code=400, detail="Prompt too large")

    result = await service.process_prompt(prompt_text)

    if not result.get("validation", {}).get("passed", False):
        return ValidationFailureResponse(
            validation=result.get("validation")
        )

    return PromptResponse(**result)
