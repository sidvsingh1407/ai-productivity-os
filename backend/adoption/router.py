import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_org, get_current_user
from models.user import User
from models.organization import Organization
from adoption.schemas import (
    AdoptionRecordCreate,
    AdoptionRecordUpdate,
    AdoptionRecordResponse,
    AdoptionRecordListResponse
)
from adoption.service import AdoptionRecordsService

router = APIRouter(tags=["Adoption Records"])
service = AdoptionRecordsService()

@router.post("/adoption-records", response_model=AdoptionRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_adoption_record(
    data: AdoptionRecordCreate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.create_record(db, current_org.id, data)

@router.get("/adoption-records", response_model=List[AdoptionRecordListResponse])
async def list_adoption_records(
    ai_system_id: Optional[uuid.UUID] = Query(None, description="Filter by AI System ID"),
    department: Optional[str] = Query(None, description="Filter by department"),
    limit: int = Query(50, ge=1, le=200, description="Max number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_records(
        db,
        current_org.id,
        ai_system_id=ai_system_id,
        department=department,
        limit=limit,
        offset=offset
    )

@router.get("/adoption-records/{record_id}", response_model=AdoptionRecordResponse)
async def get_adoption_record(
    record_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_record(db, current_org.id, record_id)

@router.put("/adoption-records/{record_id}", response_model=AdoptionRecordResponse)
async def update_adoption_record(
    record_id: uuid.UUID,
    data: AdoptionRecordUpdate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.update_record(db, current_org.id, record_id, data)

@router.delete("/adoption-records/{record_id}", status_code=status.HTTP_200_OK)
async def delete_adoption_record(
    record_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_record(db, current_org.id, record_id)
