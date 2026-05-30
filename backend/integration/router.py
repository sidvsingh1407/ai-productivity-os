import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependencies import get_current_user, get_current_org
from models.user import User
from models.organization import Organization
from .schemas import IntegrationRequest, IntegrationResultResponse
from .service import run_integration, get_integration

router = APIRouter(prefix="/integrations", tags=["integration"])

@router.post("/run", response_model=IntegrationResultResponse)
async def create_integration(
    request: IntegrationRequest,
    user: User = Depends(get_current_user),
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await run_integration(
        db=db,
        audit_id=request.audit_id,
        workflow_id=request.workflow_id,
        org_id=org.id
    )

@router.get("/{id}", response_model=IntegrationResultResponse)
async def read_integration(
    id: uuid.UUID,
    user: User = Depends(get_current_user),
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    return await get_integration(
        db=db,
        integration_id=id,
        org_id=org.id
    )
