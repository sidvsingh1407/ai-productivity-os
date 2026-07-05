import uuid
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_user, get_current_org, require_role
from models.user import User
from models.organization import Organization
from audits import schemas, service, repository
from audits.intelligence_engine import generate_intelligence
from benchmarking.adapter import get_api_benchmark_payload

router = APIRouter()

@router.post("/", response_model=schemas.AuditResponse, dependencies=[Depends(require_role("member"))])
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
        form_response=audit_in.form_response,
        evidence_response=audit_in.evidence_response,
        industry_type=audit_in.industry_type
    )

@router.get("/", response_model=schemas.AuditListResponse, dependencies=[Depends(require_role("viewer"))])
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

    # Process items to attach intelligence dynamically
    items = []
    completed_audits = await repository.get_all_completed_audits(db)

    for audit in audits:
        # Reconstruct the scores dict to pass to the intelligence engine
        scores_dict = {
            'dimensions': audit.scores or {},
            'compliance_risk_flag': audit.compliance_risk_flag,
            'compliance_risk_reasons': audit.compliance_risk_reasons or [],
            'contradictions': audit.contradictions or [],
            # In repository, missing_data_flags might not be stored directly if it's derived.
            # Assuming we can just pass an empty list if not available directly, or reconstruct if needed.
            # But wait, audit model does not have missing_data_flags stored directly!
            # Let's derive it or pass empty if not found.
            'missing_data_flags': []
        }
        industry_type_str = audit.industry_type.value if hasattr(audit.industry_type, 'value') else audit.industry_type
        intelligence = generate_intelligence(scores_dict, industry_type_str, audit.form_response)

        # We need to construct a response model manually to inject these fields
        # since they are not present in the ORM model natively.
        audit_dict = schemas.AuditResponse.model_validate(audit).model_dump()

        org_total_score = audit.total_score or 0
        org_dimension_scores = audit.scores or {}
        benchmark_payload = get_api_benchmark_payload(
            organization_total_score=org_total_score,
            organization_dimension_scores=org_dimension_scores,
            assessments=completed_audits,
            industry_type=industry_type_str
        )
        intelligence["benchmark"] = benchmark_payload

        audit_dict["intelligence"] = intelligence
        items.append(schemas.AuditResponse(**audit_dict))

    return schemas.AuditListResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{id}", response_model=schemas.AuditResponse, dependencies=[Depends(require_role("viewer"))])
async def get_single_audit(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org)
):
    """Get a single audit by ID, scoped to org."""
    audit = await repository.get_audit(db, id, current_org.id)

    scores_dict = {
        'dimensions': audit.scores or {},
        'compliance_risk_flag': audit.compliance_risk_flag,
        'compliance_risk_reasons': audit.compliance_risk_reasons or [],
        'contradictions': audit.contradictions or [],
        'missing_data_flags': []
    }
    industry_type_str = audit.industry_type.value if hasattr(audit.industry_type, 'value') else audit.industry_type
    intelligence = generate_intelligence(scores_dict, industry_type_str, audit.form_response)

    audit_dict = schemas.AuditResponse.model_validate(audit).model_dump()

    completed_audits = await repository.get_all_completed_audits(db)
    org_total_score = audit.total_score or 0
    org_dimension_scores = audit.scores or {}
    benchmark_payload = get_api_benchmark_payload(
        organization_total_score=org_total_score,
        organization_dimension_scores=org_dimension_scores,
        assessments=completed_audits,
        industry_type=industry_type_str
    )
    intelligence["benchmark"] = benchmark_payload

    audit_dict["intelligence"] = intelligence

    return schemas.AuditResponse(**audit_dict)

@router.get("/{id}/versions", response_model=List[schemas.AuditVersionResponse], dependencies=[Depends(require_role("viewer"))])
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