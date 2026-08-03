from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from database import get_db
from dependencies import get_current_org, require_role
from models.organization import Organization
from . import service
from .schemas import AgentRecommendationListResponse

router = APIRouter(prefix="/agent-recommendations", tags=["Agent Recommendations"])

@router.post("/generate", status_code=status.HTTP_200_OK, dependencies=[Depends(require_role("member"))])
async def generate_agent_recommendations_route(
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    await service.generate_and_save_agent_recommendations(db, org.id)
    return {"status": "success", "message": "Agent recommendations generated successfully."}

@router.get("/", response_model=AgentRecommendationListResponse, dependencies=[Depends(require_role("viewer"))])
async def list_agent_recommendations_route(
    opportunity_id: Optional[UUID] = None,
    agent_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_agent_recommendations(
        db=db,
        org_id=org.id,
        opportunity_id=opportunity_id,
        agent_type=agent_type,
        skip=skip,
        limit=limit
    )
