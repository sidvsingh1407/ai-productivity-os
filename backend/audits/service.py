import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from audits import repository
from audits.scoring_engine import score_response
from audits.schemas import AuditResponse
from audits.intelligence_engine import generate_intelligence
from audits.target_state_engine import generate_target_state

async def run_audit(db: AsyncSession, org_id: uuid.UUID, user_id: uuid.UUID, form_response: Dict[str, Any], evidence_response: Dict[str, Any] = None) -> AuditResponse:
    # 1. create audit record (status: running)
    audit = await repository.create_audit(db, org_id, user_id, form_response, evidence_response)

    try:
        # 2. call scoring_engine.score_response(form_response)
        scores_dict = score_response(form_response, evidence_response)

        # 3. save scores to audit record (status: complete)
        audit = await repository.save_audit_scores(db, audit.id, scores_dict)

        # 4. create audit_version record (initial version)
        await repository.create_audit_version(db, audit.id, 1, scores_dict)

        # 4.5 generate intelligence dynamically
        intelligence = generate_intelligence(scores_dict)

        # 4.6 generate target state dynamically
        target_state = generate_target_state(scores_dict)

        # 5. return AuditResponse
        return AuditResponse(
            id=audit.id,
            org_id=audit.org_id,
            user_id=audit.user_id,
            form_response=audit.form_response,
            evidence_response=audit.evidence_response,
            scores=audit.scores,
            total_score=audit.total_score,
            evidence_quality_score=audit.evidence_quality_score,
            confidence_index=audit.confidence_index,
            rating=audit.rating,
            compliance_risk_flag=audit.compliance_risk_flag,
            compliance_risk_reasons=audit.compliance_risk_reasons,
            contradictions=audit.contradictions,
            missing_data_flags=scores_dict.get('missing_data_flags', []),
            findings=intelligence.get("findings", []),
            recommendations=intelligence.get("recommendations", []),
            executive_summary=intelligence.get("executive_summary"),
            target_state=target_state,
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