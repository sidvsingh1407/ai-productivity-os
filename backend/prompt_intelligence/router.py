from fastapi import APIRouter, HTTPException, Response, Depends, BackgroundTasks
from prompt_intelligence.schemas import (
    PromptRequest, PromptResponse, ValidationFailureResponse, PromptHistoryResponse
)
from prompt_intelligence.service import PromptIntelligenceService
from typing import Union, List
from dependencies import get_current_user, get_db
from database import async_session_maker
from models.user import User
from prompt_intelligence.models import PromptHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter(tags=["Prompt Intelligence"])
service = PromptIntelligenceService()

async def log_prompt_history(user_id, original_prompt, improved_prompt):
    async with async_session_maker() as db:
        history_record = PromptHistory(
            user_id=user_id,
            original_prompt=original_prompt,
            improved_prompt=improved_prompt
        )
        db.add(history_record)
        await db.commit()

@router.post("/prompt-improver", response_model=Union[PromptResponse, ValidationFailureResponse])
async def prompt_improver(
    request: PromptRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
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

    # Save to history as background task
    improved_prompt_text = result.get("improved_prompt")
    background_tasks.add_task(log_prompt_history, current_user.id, prompt_text, improved_prompt_text)

    return PromptResponse(**result)

@router.get("/prompt-improver/history", response_model=List[PromptHistoryResponse])
async def get_prompt_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(PromptHistory).where(
        PromptHistory.user_id == current_user.id
    ).order_by(PromptHistory.created_at.desc()).limit(30)

    result = await db.execute(stmt)
    history = result.scalars().all()

    return history
