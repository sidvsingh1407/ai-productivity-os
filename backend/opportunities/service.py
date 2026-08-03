from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from . import repository
from .engine import generate_opportunities
from models.adoption_record import AdoptionRecord
from models.workflow import Workflow
from models.ai_system import AISystem
from models.engineering_record import EngineeringRecord
from sqlalchemy import select

def _row_to_dict(obj) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

async def generate_and_save_opportunities(db: AsyncSession, org_id: UUID) -> None:
    # Fetch all data sources for the org
    adoptions_q = await db.execute(select(AdoptionRecord).where(AdoptionRecord.organization_id == org_id))
    adoptions = [_row_to_dict(r) for r in adoptions_q.scalars().all()]

    workflows_q = await db.execute(select(Workflow).where(Workflow.org_id == org_id))
    workflows = [_row_to_dict(r) for r in workflows_q.scalars().all()]

    systems_q = await db.execute(select(AISystem).where(AISystem.organization_id == org_id))
    systems = [_row_to_dict(r) for r in systems_q.scalars().all()]

    eng_q = await db.execute(select(EngineeringRecord).where(EngineeringRecord.organization_id == org_id))
    eng = [_row_to_dict(r) for r in eng_q.scalars().all()]

    # Generate opportunities
    opp_dicts = generate_opportunities(adoptions, workflows, systems, eng)

    # Delete old, create new
    await repository.delete_opportunities_by_org(db, org_id)
    await repository.bulk_create_opportunities(db, opp_dicts)
    await db.commit()

async def list_opportunities(
    db: AsyncSession,
    org_id: UUID,
    ai_system_id: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
) -> dict:

    actual_sys_id = None
    if ai_system_id:
        if ai_system_id.lower() == "null":
            actual_sys_id = "null_filter"
        else:
            actual_sys_id = UUID(ai_system_id)

    items, total = await repository.list_opportunities(
        db=db,
        org_id=org_id,
        ai_system_id=actual_sys_id,
        category=category,
        skip=skip,
        limit=limit
    )

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }
