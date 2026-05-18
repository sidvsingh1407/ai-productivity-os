import uuid
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_db, get_current_user, get_current_org
from backend.models.user import User
from backend.models.organization import Organization
from backend.audits import schemas, service, repository

router = APIRouter()

@router.post("/", response_model=schemas.AuditResponse)
async def create_and_run_audit(
    audit_in: schemas.AuditCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org)
):
    """Run a new audit from form response."""
    return await service.run_audit(
        db=db,
        org_id=current_org.id,
        user_id=current_user.id,
        form_response=audit_in.form_response
    )

@router.get("/", response_model=schemas.AuditListResponse)
async def get_audits(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org)
):
    """List audits for current organization."""
    audits = await repository.list_audits(db, current_org.id, skip=skip, limit=limit)
    total = await repository.get_total_audits(db, current_org.id)

    return schemas.AuditListResponse(
        items=audits, # type: ignore (Audit -> AuditResponse conversion by pydantic)
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{id}", response_model=schemas.AuditResponse)
async def get_single_audit(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org)
):
    """Get a single audit by ID, scoped to org."""
    audit = await repository.get_audit(db, id, current_org.id)
    return audit # type: ignore

@router.get("/{id}/versions", response_model=List[schemas.AuditVersionResponse])
async def get_audit_versions(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org)
):
    """List versions for a specific audit."""
    # First verify the audit belongs to the org
    await repository.get_audit(db, id, current_org.id)
    # Then get versions
    versions = await repository.list_audit_versions(db, id)
    return versions