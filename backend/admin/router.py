from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from database import get_db
from dependencies import require_superadmin
from admin import service
from admin.schemas import UserResponse, OrgResponse, SystemStatsResponse, LeadPaginatedResponse, UserPaginatedResponse, OrgPaginatedResponse

router = APIRouter()

@router.get("/users", response_model=UserPaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    _=Depends(require_superadmin)
):
    return await service.list_all_users(db, page=page, limit=limit)

@router.get("/orgs", response_model=OrgPaginatedResponse)
async def list_orgs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    _=Depends(require_superadmin)
):
    return await service.list_all_orgs(db, page=page, limit=limit)

@router.put("/users/{id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_superadmin)
):
    user = await service.deactivate_user(db, user_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/stats", response_model=SystemStatsResponse)
async def system_stats(
    db: AsyncSession = Depends(get_db),
    _=Depends(require_superadmin)
):
    stats = await service.get_system_stats(db)
    return stats

@router.get("/leads", response_model=LeadPaginatedResponse)
async def list_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    _=Depends(require_superadmin)
):
    return await service.list_all_leads(db, skip=skip, limit=limit)
