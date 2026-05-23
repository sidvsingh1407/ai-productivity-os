import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from audits import repository
from audits.scoring_engine import score_response
from audits.schemas import AuditResponse

async def run_audit(db: AsyncSession, org_id: uuid.UUID, user_id: uuid.UUID, form_response: Dict[str, Any]) -> AuditResponse:
    # 1. create audit record (status: running)
    audit = await repository.create_audit(db, org_id, user_id, form_response)

    try:
        # 2. call scoring_engine.score_response(form_response)
        scores_dict = score_response(form_response)

        # 3. save scores to audit record (status: complete)
        audit = await repository.save_audit_scores(db, audit.id, scores_dict)

        # 4. create audit_version record (initial version)
        await repository.create_audit_version(db, audit.id, 1, scores_dict)

        # 5. return AuditResponse
        return AuditResponse(
            id=audit.id,
            org_id=audit.org_id,
            user_id=audit.user_id,
            scores=audit.scores,
            total_score=audit.total_score,
            rating=audit.rating,
            compliance_risk_flag=audit.compliance_risk_flag,
            compliance_risk_reasons=audit.compliance_risk_reasons,
            contradictions=scores_dict.get('contradictions', []),
            missing_data_flags=scores_dict.get('missing_data_flags', []),
            status=audit.status,
            created_at=audit.created_at
        )

    except Exception as e:
        # Update status to failed if something goes wrong
        audit.status = repository.AuditStatus.failed
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit failed: {str(e)}"
        )