from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import uuid

from .dependencies import verify_api_key
from .middleware import APIKeyRoute
from .schemas import AuditApiRequest, RiskApiRequest
from models.api_platform import ApiKey
from models.organization import OrgRole
from organizations.repository import OrganizationRepository
from audits.repository import get_audit, AuditStatus
from audits.scoring_engine import score_response
from audits.intelligence_engine import generate_intelligence

from audits.service import run_audit
from audits.schemas import AuditResponse, RiskProjection
from audits.risk_projection_engine import generate_risk_projection

router = APIRouter(route_class=APIKeyRoute, tags=["Public API"])

async def get_user_id_for_api_key(db: AsyncSession, organization_id: uuid.UUID) -> uuid.UUID:
    org_repo = OrganizationRepository(db)
    members = await org_repo.get_members(organization_id)

    if not members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization has no active user available for audit attribution."
        )

    # Priority: Owner > Admin > Member > Viewer
    role_priority = {
        OrgRole.owner: 1,
        OrgRole.admin: 2,
        OrgRole.member: 3,
        OrgRole.viewer: 4
    }

    # Sort members by role priority, then by joined_at (earliest first)
    sorted_members = sorted(members, key=lambda m: (role_priority.get(m.role, 99), m.joined_at))
    return sorted_members[0].user_id

@router.post("/audit", response_model=AuditResponse)
async def create_audit_api(
    request: AuditApiRequest,
    api_key: ApiKey = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit an assessment payload and receive intelligence through the AI Audit API.
    """
    user_id = await get_user_id_for_api_key(db, api_key.organization_id)

    audit_response = await run_audit(
        db=db,
        org_id=api_key.organization_id,
        user_id=user_id,
        form_response=request.form_response,
        evidence_response=request.evidence_response,
        industry_type=request.industry_type
    )

    return audit_response

@router.post("/risk", response_model=RiskProjection)
async def generate_risk_api(
    request: RiskApiRequest,
    api_key: ApiKey = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate future-state risk projections.
    """
    audit = await get_audit(db, request.audit_id, api_key.organization_id)

    if audit.status != AuditStatus.complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Risk projection requires a completed audit."
        )

    scores_dict = score_response(audit.form_response, audit.evidence_response)

    industry_type_str = audit.industry_type.value if hasattr(audit.industry_type, 'value') else audit.industry_type

    intelligence = generate_intelligence(scores_dict, industry_type_str)

    return intelligence["risk_projection"]
