import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_org, get_current_user
from models.user import User
from models.organization import Organization
from prompt_engineer_subscriptions.schemas import (
    PromptEngineerSubscriptionCreate,
    PromptEngineerSubscriptionUpdate,
    PromptEngineerSubscriptionResponse,
    PromptEngineerSubscriptionListResponse
)
from prompt_engineer_subscriptions.service import PromptEngineerSubscriptionsService

router = APIRouter(tags=["Prompt Engineer Subscriptions"])
service = PromptEngineerSubscriptionsService()

@router.post("/prompt-engineer-subscriptions", response_model=PromptEngineerSubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    data: PromptEngineerSubscriptionCreate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.create_subscription(db, current_org.id, data)

@router.get("/prompt-engineer-subscriptions", response_model=List[PromptEngineerSubscriptionListResponse])
async def list_subscriptions(
    limit: int = Query(50, ge=1, le=200, description="Max number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_subscriptions(db, current_org.id, limit=limit, offset=offset)

@router.get("/prompt-engineer-subscriptions/{subscription_id}", response_model=PromptEngineerSubscriptionResponse)
async def get_subscription(
    subscription_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_subscription(db, current_org.id, subscription_id)

@router.put("/prompt-engineer-subscriptions/{subscription_id}", response_model=PromptEngineerSubscriptionResponse)
async def update_subscription(
    subscription_id: uuid.UUID,
    data: PromptEngineerSubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.update_subscription(db, current_org.id, subscription_id, data)

@router.delete("/prompt-engineer-subscriptions/{subscription_id}", status_code=status.HTTP_200_OK)
async def delete_subscription(
    subscription_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_subscription(db, current_org.id, subscription_id)
