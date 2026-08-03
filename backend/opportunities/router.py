from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from database import get_db
from dependencies import get_current_user, get_current_org, require_role
from models.user import User
from models.organization import Organization
from . import service
from .schemas import OpportunityListResponse, OpportunityCategory

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])

@router.post("/generate", status_code=status.HTTP_200_OK, dependencies=[Depends(require_role("member"))])
async def generate_opportunities_endpoint(
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    """
    Generate opportunities from all confirmed data sources.
    """
    await service.generate_and_save_opportunities(db, org.id)
    return {"status": "success", "message": "Opportunities generated successfully."}

@router.get("/", response_model=OpportunityListResponse, dependencies=[Depends(require_role("viewer"))])
async def list_opportunities_endpoint(
    ai_system_id: Optional[str] = Query(None, description="Pass 'null' for org-level only, or a valid UUID"),
    category: Optional[OpportunityCategory] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    """
    List opportunities for the organization.
    """
    result = await service.list_opportunities(
        db=db,
        org_id=org.id,
        ai_system_id=ai_system_id,
        category=category,
        skip=skip,
        limit=limit
    )
    return result
