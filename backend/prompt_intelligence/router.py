from fastapi import APIRouter, HTTPException, Response, Depends
from prompt_intelligence.schemas import PromptRequest, PromptResponse, ValidationFailureResponse
from prompt_intelligence.service import PromptIntelligenceService
from typing import Union
from dependencies import get_current_user
from models.user import User

router = APIRouter(tags=["Prompt Intelligence"])
service = PromptIntelligenceService()

@router.post("/prompt-improver", response_model=Union[PromptResponse, ValidationFailureResponse])
async def prompt_improver(
    request: PromptRequest,
    current_user: User = Depends(get_current_user)
):
    prompt_text = request.prompt.strip()

    if not prompt_text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    if len(prompt_text) > 10000:
        raise HTTPException(status_code=400, detail="Prompt too large")

    result = await service.process_prompt(prompt_text)

    # ValidationFailureResponse is explicitly an object with "validation" key where validation is ValidationResponse
    if not result.get("validation", {}).get("passed", False):
        return Response(
            status_code=400,
            content=ValidationFailureResponse(validation=result.get("validation")).model_dump_json(),
            media_type="application/json"
        )

    return PromptResponse(**result)
