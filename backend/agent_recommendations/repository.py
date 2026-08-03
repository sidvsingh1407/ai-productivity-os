from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from uuid import UUID
from typing import List, Dict, Any, Optional, Tuple
from models.agent_recommendation import AgentRecommendation
from .schemas import AgentRecommendationResponse

async def delete_recommendations_by_org(db: AsyncSession, org_id: UUID) -> None:
    await db.execute(delete(AgentRecommendation).where(AgentRecommendation.organization_id == org_id))

async def bulk_create_recommendations(db: AsyncSession, data: List[Dict[str, Any]]) -> None:
    if not data:
        return

    recs = [AgentRecommendation(**item) for item in data]
    db.add_all(recs)

async def list_agent_recommendations(
    db: AsyncSession,
    org_id: UUID,
    opportunity_id: Optional[UUID] = None,
    agent_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
) -> Tuple[List[AgentRecommendationResponse], int]:

    query = select(AgentRecommendation).where(AgentRecommendation.organization_id == org_id)
    count_query = select(func.count()).select_from(AgentRecommendation).where(AgentRecommendation.organization_id == org_id)

    if opportunity_id:
        query = query.where(AgentRecommendation.opportunity_id == opportunity_id)
        count_query = count_query.where(AgentRecommendation.opportunity_id == opportunity_id)

    if agent_type:
        query = query.where(AgentRecommendation.agent_type == agent_type)
        count_query = count_query.where(AgentRecommendation.agent_type == agent_type)

    query = query.order_by(AgentRecommendation.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    count_result = await db.execute(count_query)

    items = result.scalars().all()
    total = count_result.scalar_one()

    return [AgentRecommendationResponse.model_validate(item) for item in items], total
