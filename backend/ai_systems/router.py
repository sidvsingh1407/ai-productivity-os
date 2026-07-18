import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_org, get_current_user
from models.user import User
from models.organization import Organization
from ai_systems.schemas import AISystemCreate, AISystemUpdate, AISystemResponse, AISystemListResponse
from ai_systems.service import AISystemsService

router = APIRouter(tags=["AI Systems"])
service = AISystemsService()

@router.post("/ai-systems", response_model=AISystemResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_system(
    data: AISystemCreate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.create_system(db, current_org.id, data)

@router.get("/ai-systems", response_model=List[AISystemListResponse])
async def list_ai_systems(
    limit: int = Query(50, ge=1, le=200, description="Max number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_systems(db, current_org.id, limit=limit, offset=offset)

@router.get("/ai-systems/{system_id}", response_model=AISystemResponse)
async def get_ai_system(
    system_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_system(db, current_org.id, system_id)

@router.put("/ai-systems/{system_id}", response_model=AISystemResponse)
async def update_ai_system(
    system_id: uuid.UUID,
    data: AISystemUpdate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.update_system(db, current_org.id, system_id, data)

@router.delete("/ai-systems/{system_id}", status_code=status.HTTP_200_OK)
async def delete_ai_system(
    system_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_system(db, current_org.id, system_id)
