from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from database import get_db
from dependencies import get_current_user, get_current_org, require_role
from models.user import User
from models.organization import Organization
from . import service
from . import repository
from .schemas import WorkflowCreate, WorkflowDetailResponse, WorkflowResponse, WorkflowIntelligence
from .workflow_intelligence_engine import generate_workflow_intelligence

router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.post("/", response_model=WorkflowDetailResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("member"))])
async def create_and_run_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    org: Organization = Depends(get_current_org)
):
    """
    Run a diagnostic workflow pipeline.
    """
    return await service.run_workflow(
        db=db,
        org_id=org["id"],
        user_id=user["id"],
        input_config=payload.input_config
    )

@router.get("/", response_model=List[WorkflowResponse], dependencies=[Depends(require_role("viewer"))])
async def list_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    """
    List all diagnostic workflows for the current organization.
    """
    workflows = await repository.list_workflows(db=db, org_id=org.id, skip=skip, limit=limit)
    return [WorkflowResponse.model_validate(w) for w in workflows]

@router.get("/{workflow_id}", response_model=WorkflowDetailResponse, dependencies=[Depends(require_role("viewer"))])
async def get_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    """
    Get a specific workflow and its blueprints by ID.
    """
    workflow = await repository.get_workflow(db=db, workflow_id=workflow_id, org_id=org.id)
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )

    blueprints = await repository.get_workflow_blueprints(db=db, workflow_id=workflow_id)

    intelligence_payload = generate_workflow_intelligence(workflow.input_config)
    intelligence = WorkflowIntelligence(**intelligence_payload)

    workflow_resp = WorkflowResponse.model_validate(workflow)
    return WorkflowDetailResponse(
        **workflow_resp.model_dump(),
        blueprints=blueprints,
        intelligence=intelligence
    )
