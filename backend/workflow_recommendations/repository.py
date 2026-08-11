from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from uuid import UUID
from typing import List, Dict, Any, Optional, Tuple
from models.workflow_recommendation import WorkflowRecommendation
from .schemas import WorkflowRecommendationResponse

async def delete_recommendations_by_org(db: AsyncSession, org_id: UUID) -> None:
    await db.execute(delete(WorkflowRecommendation).where(WorkflowRecommendation.organization_id == org_id))

async def bulk_create_recommendations(db: AsyncSession, data: List[Dict[str, Any]]) -> None:
    if not data:
        return

    recs = [WorkflowRecommendation(**item) for item in data]
    db.add_all(recs)

async def list_workflow_recommendations(
    db: AsyncSession,
    org_id: UUID,
    opportunity_id: Optional[UUID] = None,
    recommendation_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
) -> Tuple[List[WorkflowRecommendationResponse], int]:

    query = select(WorkflowRecommendation).where(WorkflowRecommendation.organization_id == org_id)
    count_query = select(func.count()).select_from(WorkflowRecommendation).where(WorkflowRecommendation.organization_id == org_id)

    if opportunity_id:
        query = query.where(WorkflowRecommendation.opportunity_id == opportunity_id)
        count_query = count_query.where(WorkflowRecommendation.opportunity_id == opportunity_id)

    if recommendation_type:
        query = query.where(WorkflowRecommendation.recommendation_type == recommendation_type)
        count_query = count_query.where(WorkflowRecommendation.recommendation_type == recommendation_type)

    query = query.order_by(WorkflowRecommendation.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    count_result = await db.execute(count_query)

    items = result.scalars().all()
    total = count_result.scalar_one()

    return [WorkflowRecommendationResponse.model_validate(item) for item in items], total
