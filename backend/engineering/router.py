import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_org, get_current_user
from models.user import User
from models.organization import Organization
from engineering.schemas import (
    EngineeringRecordCreate,
    EngineeringRecordUpdate,
    EngineeringRecordResponse,
    EngineeringRecordListResponse
)
from engineering.service import EngineeringRecordsService

router = APIRouter(tags=["Engineering Intelligence"])
service = EngineeringRecordsService()

@router.post("/engineering-records", response_model=EngineeringRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_engineering_record(
    data: EngineeringRecordCreate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.create_record(db, current_org.id, data)

@router.get("/engineering-records", response_model=List[EngineeringRecordListResponse])
async def list_engineering_records(
    limit: int = Query(50, ge=1, le=200, description="Max number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_records(
        db,
        current_org.id,
        limit=limit,
        offset=offset
    )

@router.get("/engineering-records/{record_id}", response_model=EngineeringRecordResponse)
async def get_engineering_record(
    record_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_record(db, current_org.id, record_id)

@router.put("/engineering-records/{record_id}", response_model=EngineeringRecordResponse)
async def update_engineering_record(
    record_id: uuid.UUID,
    data: EngineeringRecordUpdate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.update_record(db, current_org.id, record_id, data)

@router.delete("/engineering-records/{record_id}", status_code=status.HTTP_200_OK)
async def delete_engineering_record(
    record_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_record(db, current_org.id, record_id)
