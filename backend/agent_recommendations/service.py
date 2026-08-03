from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from sqlalchemy import select
from models.opportunity import Opportunity
from models.ai_system import AISystem
from . import repository
from .engine import generate_agent_recommendations

def _row_to_dict(obj) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

async def generate_and_save_agent_recommendations(db: AsyncSession, org_id: UUID) -> None:
    # Fetch all opportunities for the org and join their system's department if available
    # Since we need to know the department, we can do a left join
    query = select(Opportunity, AISystem.department).outerjoin(
        AISystem, Opportunity.ai_system_id == AISystem.id
    ).where(Opportunity.organization_id == org_id)

    result = await db.execute(query)
    rows = result.all()

    opportunities_data = []
    for opp, dept in rows:
        opp_dict = _row_to_dict(opp)
        opp_dict["department"] = dept
        opportunities_data.append(opp_dict)

    # Generate recommendations via engine
    recs = generate_agent_recommendations(opportunities_data)

    # Save to db
    await repository.delete_recommendations_by_org(db, org_id)
    await repository.bulk_create_recommendations(db, recs)
    await db.commit()

async def list_agent_recommendations(
    db: AsyncSession,
    org_id: UUID,
    opportunity_id: Optional[UUID] = None,
    agent_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
) -> dict:

    items, total = await repository.list_agent_recommendations(
        db=db,
        org_id=org_id,
        opportunity_id=opportunity_id,
        agent_type=agent_type,
        skip=skip,
        limit=limit
    )

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }
