import uuid
from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.roadmap_item import RoadmapItem
from models.opportunity import Opportunity
from models.agent_recommendation import AgentRecommendation
from models.workflow_recommendation import WorkflowRecommendation

TIME_HORIZON_MAPPING = {
    "High": "30_day",
    "Medium": "90_day",
    "Low": "1_year"
}

async def generate_roadmap_items(db_session: AsyncSession, organization_id: uuid.UUID) -> List[RoadmapItem]:
    # 1. Idempotency: clear existing "general" category roadmap items for this org
    stmt = delete(RoadmapItem).where(
        RoadmapItem.organization_id == organization_id,
        RoadmapItem.category == "general"
    )
    await db_session.execute(stmt)

    roadmap_items = []

    # 2. Opportunities
    opp_stmt = select(Opportunity).where(Opportunity.organization_id == organization_id)
    opp_result = await db_session.execute(opp_stmt)
    opportunities = opp_result.scalars().all()

    for opp in opportunities:
        priority = opp.confidence_or_priority
        if priority not in TIME_HORIZON_MAPPING:
            continue

        time_horizon = TIME_HORIZON_MAPPING[priority]

        item = RoadmapItem(
            organization_id=organization_id,
            source_type="opportunity",
            opportunity_id=opp.id,
            agent_recommendation_id=None,
            workflow_recommendation_id=None,
            category="general",
            time_horizon=time_horizon,
            title=opp.title,
            description=opp.description,
            department=None,
            owner=None
        )
        roadmap_items.append(item)

    # 3. Agent Recommendations
    ar_stmt = select(AgentRecommendation).where(AgentRecommendation.organization_id == organization_id)
    ar_result = await db_session.execute(ar_stmt)
    agent_recommendations = ar_result.scalars().all()

    for ar in agent_recommendations:
        priority = ar.confidence
        if priority not in TIME_HORIZON_MAPPING:
            continue

        time_horizon = TIME_HORIZON_MAPPING[priority]

        item = RoadmapItem(
            organization_id=organization_id,
            source_type="agent_recommendation",
            opportunity_id=None,
            agent_recommendation_id=ar.id,
            workflow_recommendation_id=None,
            category="general",
            time_horizon=time_horizon,
            title=ar.agent_type,
            description=ar.rationale,
            department=None,
            owner=None
        )
        roadmap_items.append(item)

    # 4. Workflow Recommendations
    wr_stmt = select(WorkflowRecommendation).where(WorkflowRecommendation.organization_id == organization_id)
    wr_result = await db_session.execute(wr_stmt)
    workflow_recommendations = wr_result.scalars().all()

    for wr in workflow_recommendations:
        priority = wr.confidence
        if priority not in TIME_HORIZON_MAPPING:
            continue

        time_horizon = TIME_HORIZON_MAPPING[priority]

        item = RoadmapItem(
            organization_id=organization_id,
            source_type="workflow_recommendation",
            opportunity_id=None,
            agent_recommendation_id=None,
            workflow_recommendation_id=wr.id,
            category="general",
            time_horizon=time_horizon,
            title=wr.recommendation_type,
            description=wr.rationale,
            department=None,
            owner=None
        )
        roadmap_items.append(item)

    if roadmap_items:
        db_session.add_all(roadmap_items)

    return roadmap_items
