from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from database import get_db
from dependencies import get_current_user, get_current_org
from analytics import service
from analytics.schemas import ScoreTrendItem, DimensionAverages, AuditVolume, ComplianceRate

router = APIRouter()

@router.get("/scores", response_model=list[ScoreTrendItem])
async def get_scores(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_org: Dict[str, Any] = Depends(get_current_org),
    _=Depends(get_current_user)
):
    # Depending on mock vs real, org id might be a string or UUID.
    org_id = current_org["id"]
    return await service.get_score_trend(db, org_id=org_id, days=days)

@router.get("/dimensions", response_model=DimensionAverages)
async def get_dimensions(
    db: AsyncSession = Depends(get_db),
    current_org: Dict[str, Any] = Depends(get_current_org),
    _=Depends(get_current_user)
):
    org_id = current_org["id"]
    return await service.get_dimension_averages(db, org_id=org_id)

@router.get("/volume", response_model=AuditVolume)
async def get_volume(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_org: Dict[str, Any] = Depends(get_current_org),
    _=Depends(get_current_user)
):
    org_id = current_org["id"]
    return await service.get_audit_volume(db, org_id=org_id, days=days)

@router.get("/compliance", response_model=ComplianceRate)
async def get_compliance(
    db: AsyncSession = Depends(get_db),
    current_org: Dict[str, Any] = Depends(get_current_org),
    _=Depends(get_current_user)
):
    org_id = current_org["id"]
    return await service.get_compliance_rate(db, org_id=org_id)
