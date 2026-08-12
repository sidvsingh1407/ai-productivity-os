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

    # Fetch per-system findings
    db_system_findings = await repository.get_system_findings_by_audit(db, id)
    system_findings_responses = [
        {
            "ai_system_id": sf.ai_system_id,
            "ai_system_name": sf.ai_system.name,
            "findings": sf.findings,
            "recommendations": sf.recommendations,
            "executive_summary": sf.executive_summary,
            "dimension_scores": sf.dimension_scores
        }
        for sf in db_system_findings
    ]
    audit_dict["system_findings"] = system_findings_responses

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

@router.patch("/{id}/system-findings/{system_finding_id}/findings/{finding_title}", response_model=schemas.SystemFindingResponse, dependencies=[Depends(require_role("member"))])
async def update_system_finding_finding_route(
    id: uuid.UUID,
    system_finding_id: uuid.UUID,
    finding_title: str,
    update_data: schemas.FindingPatchUpdate,
    db: AsyncSession = Depends(get_db),
    current_org: Organization = Depends(get_current_org)
):
    """Update a specific finding within a system finding."""
    update_dict = update_data.model_dump(exclude_unset=True)

    updated_sf = await service.update_system_finding(
        db=db,
        audit_id=id,
        org_id=current_org.id,
        system_finding_id=system_finding_id,
        finding_title=finding_title,
        update_data=update_dict
    )

    return {
        "ai_system_id": updated_sf.ai_system_id,
        "ai_system_name": updated_sf.ai_system.name if hasattr(updated_sf, 'ai_system') and updated_sf.ai_system else "",
        "findings": updated_sf.findings,
        "recommendations": updated_sf.recommendations,
        "executive_summary": updated_sf.executive_summary,
        "dimension_scores": updated_sf.dimension_scores
    }