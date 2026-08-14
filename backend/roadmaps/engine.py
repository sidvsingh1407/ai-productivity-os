import uuid
from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.roadmap_item import RoadmapItem
from models.opportunity import Opportunity
from models.agent_recommendation import AgentRecommendation
from models.workflow_recommendation import WorkflowRecommendation
from models.ai_system import AISystem
from models.risk_classification import RiskClassification
from models.dependency_map import DependencyNode, DependencyEdge
from sqlalchemy import or_, func

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

async def generate_governance_roadmap_items(db_session: AsyncSession, organization_id: uuid.UUID) -> List[RoadmapItem]:
    # 1. Idempotency: clear existing "governance" category roadmap items for this org
    stmt = delete(RoadmapItem).where(
        RoadmapItem.organization_id == organization_id,
        RoadmapItem.category == "governance"
    )
    await db_session.execute(stmt)

    roadmap_items = []

    # 2. Fetch Systems and Compute Governance Flags
    sys_stmt = select(AISystem).where(AISystem.organization_id == organization_id)
    sys_result = await db_session.execute(sys_stmt)
    systems = sys_result.scalars().all()

    for system in systems:
        # Fetch its latest RiskClassification using created_at DESC
        risk_stmt = select(RiskClassification).where(
            RiskClassification.ai_system_id == system.id
        ).order_by(RiskClassification.created_at.desc()).limit(1)
        risk_result = await db_session.execute(risk_stmt)
        risk_classification = risk_result.scalar_one_or_none()

        if not risk_classification or risk_classification.risk_level == "minimal_risk":
            continue

        # Fetch the corresponding DependencyNode
        node_stmt = select(DependencyNode).where(
            DependencyNode.ai_system_id == system.id
        )
        node_result = await db_session.execute(node_stmt)
        node = node_result.scalar_one_or_none()

        if not node:
            continue

        # Count total connected edges (both directions, all edge_types)
        # Note: This represents total connected degree as a proxy for blast radius, as agreed.
        # Future refinement can split by direction/type once there's a clearer governance definition.
        edge_stmt = select(func.count(DependencyEdge.id)).where(
            or_(
                DependencyEdge.source_node_id == node.id,
                DependencyEdge.target_node_id == node.id
            )
        )
        edge_result = await db_session.execute(edge_stmt)
        dependency_count = edge_result.scalar() or 0

        if dependency_count >= 5:
            # 3. Generate Roadmap Items for Flagged Systems
            # We look for ANY Phase 7 record associated with this system.
            # Easiest way: look for an Opportunity tied to this AI System
            opp_stmt = select(Opportunity).where(Opportunity.ai_system_id == system.id).limit(1)
            opp_result = await db_session.execute(opp_stmt)
            opp = opp_result.scalar_one_or_none()

            source_type = None
            opp_id = None
            ar_id = None
            wr_id = None

            if opp:
                source_type = "opportunity"
                opp_id = opp.id
            else:
                # As noted, AgentRecommendation and WorkflowRecommendation don't have ai_system_id directly, they have opportunity_id.
                # Thus if there's no opportunity_id for this ai_system_id, there logically can be no agent/workflow recs
                # for this ai_system_id because they only join through Opportunity.
                pass

            if not source_type:
                # Known gap: structurally possible for a system to be governance-flag-worthy with no Phase 7 source record
                # to attach to; roadmap_items schema currently requires one. We skip in this case.
                continue

            item = RoadmapItem(
                organization_id=organization_id,
                source_type=source_type,
                opportunity_id=opp_id,
                agent_recommendation_id=ar_id,
                workflow_recommendation_id=wr_id,
                category="governance",
                time_horizon="30_day",
                title="Governance Escalation",
                description=f"System flagged due to risk level '{risk_classification.risk_level}' and {dependency_count} dependencies.",
                department=None,
                owner=None
            )
            roadmap_items.append(item)

    if roadmap_items:
        db_session.add_all(roadmap_items)

    return roadmap_items
