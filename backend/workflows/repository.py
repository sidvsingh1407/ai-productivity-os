from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any, Optional

from models.workflow import Workflow, Blueprint

async def create_workflow(db: AsyncSession, org_id: str, user_id: str, input_config: Dict[str, Any]) -> Workflow:
    workflow = Workflow(
        org_id=org_id,
        user_id=user_id,
        status="running",
        input_config=input_config
    )
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return workflow

async def save_blueprints(db: AsyncSession, workflow_id: str, blueprints: List[Dict[str, Any]]) -> List[Blueprint]:
    saved_blueprints = []
    for bp_data in blueprints:
        blueprint = Blueprint(
            workflow_id=workflow_id,
            process_id=bp_data["process_id"],
            automation_tier=bp_data["automation_tier"],
            industry_variant=bp_data.get("industry_variant"),
            confidence=bp_data["confidence"],
            merged=bp_data.get("merged", False),
            blueprint_data=bp_data["blueprint_data"]
        )
        db.add(blueprint)
        saved_blueprints.append(blueprint)

    if saved_blueprints:
        await db.commit()
        for bp in saved_blueprints:
            await db.refresh(bp)

    return saved_blueprints

async def get_workflow(db: AsyncSession, workflow_id: str, org_id: str) -> Optional[Workflow]:
    query = select(Workflow).where(Workflow.id == workflow_id, Workflow.org_id == org_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_workflow_blueprints(db: AsyncSession, workflow_id: str) -> List[Blueprint]:
    query = select(Blueprint).where(Blueprint.workflow_id == workflow_id)
    result = await db.execute(query)
    return list(result.scalars().all())

async def list_workflows(db: AsyncSession, org_id: str, skip: int = 0, limit: int = 20) -> List[Workflow]:
    query = select(Workflow).where(Workflow.org_id == org_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())

async def update_workflow_status(db: AsyncSession, workflow: Workflow, status: str) -> Workflow:
    workflow.status = status
    await db.commit()
    await db.refresh(workflow)
    return workflow
