import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from audits import repository
from audits.scoring_engine import score_response
from audits.schemas import AuditResponse
from audits.intelligence_engine import generate_intelligence
from benchmarking.adapter import get_api_benchmark_payload
from services.narrative_service import generate_audit_narrative

async def run_audit(db: AsyncSession, org_id: uuid.UUID, user_id: uuid.UUID, form_response: Dict[str, Any], evidence_response: Dict[str, Any] = None, industry_type: str = None) -> AuditResponse:
    # 1. create audit record (status: running)
    audit = await repository.create_audit(db, org_id, user_id, form_response, evidence_response, industry_type)

    try:
        # 2. call scoring_engine.score_response(form_response)
        scores_dict = score_response(form_response, evidence_response)

        # 3. save scores to audit record (status: complete)
        audit = await repository.save_audit_scores(db, audit.id, scores_dict)

        # 4. create audit_version record (initial version)
        await repository.create_audit_version(db, audit.id, 1, scores_dict)

        # 4.5 generate intelligence dynamically
        industry_type_str = audit.industry_type.value if hasattr(audit.industry_type, 'value') else audit.industry_type
        intelligence = generate_intelligence(scores_dict, industry_type_str, form_response)

        # 4.6 append benchmark intelligence
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

        # 4.7 Generate dynamic narrative
        company_context = {
            "company_name": form_response.get("companyName", "the organization"),
            "industry": form_response.get("industry", industry_type_str or "unspecified"),
            "company_size": form_response.get("companySize", "unspecified"),
            "region": form_response.get("region", "unspecified"),
            "ai_usage_description": form_response.get("primaryAiUsage", "unspecified"),
            "governance_status": form_response.get("governanceMaturity", "unspecified")
        }

        narrative_scores = {
            "overall_score": audit.total_score or 0,
            "awareness_score": org_dimension_scores.get("awareness", 0) * 5,
            "adoption_score": org_dimension_scores.get("adoption", 0) * 5,
            "integration_score": org_dimension_scores.get("integration", 0) * 5,
            "governance_score": org_dimension_scores.get("governance", 0) * 5,
            "roi_score": org_dimension_scores.get("roi", 0) * 5,
        }

        narrative = await generate_audit_narrative(narrative_scores, company_context)

        narrative_source = "static"
        if narrative:
            narrative_source = "dynamic"
            if "executive_summary" in narrative:
                # Update executive summary fields if present
                for key in ["overall_assessment", "critical_risk", "primary_opportunity", "recommended_first_action"]:
                    if key in narrative["executive_summary"]:
                        intelligence["executive_summary"][key] = narrative["executive_summary"][key]

            if "roadmap" in narrative:
                intelligence["roadmap"] = narrative["roadmap"]

            if "recommendations" in narrative:
                intelligence["recommendations"] = narrative["recommendations"]

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
            intelligence=intelligence,
            narrative_source=narrative_source,
            status=audit.status,
            industry_type=audit.industry_type,
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