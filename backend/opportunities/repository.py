from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
from typing import List, Optional
from models.opportunity import Opportunity
from .schemas import OpportunityCategory

async def create_opportunity(db: AsyncSession, data: dict) -> Opportunity:
    opp = Opportunity(**data)
    db.add(opp)
    await db.flush()
    return opp

async def bulk_create_opportunities(db: AsyncSession, data_list: List[dict]) -> List[Opportunity]:
    if not data_list:
        return []
    opps = [Opportunity(**data) for data in data_list]
    db.add_all(opps)
    await db.flush()
    return opps

async def delete_opportunities_by_org(db: AsyncSession, org_id: UUID) -> None:
    # We rebuild the opportunities for an org from scratch
    # In a full production system, we'd do smart diffing.
    # Here we clear and recreate.
    result = await db.execute(select(Opportunity).where(Opportunity.organization_id == org_id))
    opps = result.scalars().all()
    for opp in opps:
        await db.delete(opp)
    await db.flush()

async def list_opportunities(
    db: AsyncSession,
    org_id: UUID,
    ai_system_id: Optional[str | UUID] = None,
    category: Optional[OpportunityCategory] = None,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[Opportunity], int]:

    query = select(Opportunity).where(Opportunity.organization_id == org_id)

    if ai_system_id == "null_filter":
        query = query.where(Opportunity.ai_system_id == None)
    elif ai_system_id is not None:
        query = query.where(Opportunity.ai_system_id == ai_system_id)

    if category is not None:
        query = query.where(Opportunity.category == category)

    from sqlalchemy import func
    total = await db.scalar(select(func.count()).select_from(query.subquery()))

    query = query.order_by(Opportunity.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)

    return list(result.scalars().all()), total or 0
