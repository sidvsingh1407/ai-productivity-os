from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from sqlalchemy import select
from models.opportunity import Opportunity
from . import repository
from .engine import generate_workflow_recommendations

def _row_to_dict(obj) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

async def generate_and_save_workflow_recommendations(db: AsyncSession, org_id: UUID) -> None:
    # Fetch all opportunities for the org
    query = select(Opportunity).where(Opportunity.organization_id == org_id)

    result = await db.execute(query)
    opportunities = result.scalars().all()

    opportunities_data = [_row_to_dict(opp) for opp in opportunities]

    # Generate recommendations via engine
    recs = generate_workflow_recommendations(opportunities_data)

    # Save to db
    await repository.delete_recommendations_by_org(db, org_id)
    await repository.bulk_create_recommendations(db, recs)
    await db.commit()

async def list_workflow_recommendations(
    db: AsyncSession,
    org_id: UUID,
    opportunity_id: Optional[UUID] = None,
    recommendation_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
) -> dict:

    items, total = await repository.list_workflow_recommendations(
        db=db,
        org_id=org_id,
        opportunity_id=opportunity_id,
        recommendation_type=recommendation_type,
        skip=skip,
        limit=limit
    )

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }
