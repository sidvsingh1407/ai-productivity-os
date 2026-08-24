import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from audits import repository
from audits.scoring_engine import score_response
from audits.schemas import AuditResponse
from audits.intelligence_engine import generate_intelligence, aggregate_top_findings_and_recommendations
from audits.roadmap_engine import generate_system_driven_roadmap
from benchmarking.adapter import get_api_benchmark_payload
from financial.calculator import calculate_system_cost
from services.narrative_service import generate_audit_narrative


async def run_audit(
    db: AsyncSession,
    org_id: uuid.UUID,
    user_id: uuid.UUID,
    form_response: Dict[str, Any],
    evidence_response: Dict[str, Any] = None,
    industry_type: str = None,
) -> AuditResponse:
    # 1. create audit record (status: running)
    audit = await repository.create_audit(
        db, org_id, user_id, form_response, evidence_response, industry_type
    )

    try:
        # 2. call scoring_engine.score_response(form_response)
        scores_dict = score_response(form_response, evidence_response)

        # 3. save scores to audit record (status: complete)
        audit = await repository.save_audit_scores(db, audit.id, scores_dict)

        # 4. create audit_version record (initial version)
        await repository.create_audit_version(db, audit.id, 1, scores_dict)

        # 4.5 generate intelligence dynamically
        industry_type_str = (
            audit.industry_type.value
            if hasattr(audit.industry_type, "value")
            else audit.industry_type
        )
        intelligence = generate_intelligence(
            scores_dict, industry_type_str, form_response
        )

        # 4.6 append benchmark intelligence
        completed_audits = await repository.get_all_completed_audits(db)
        org_total_score = audit.total_score or 0
        org_dimension_scores = audit.scores or {}
        benchmark_payload = get_api_benchmark_payload(
            organization_total_score=org_total_score,
            organization_dimension_scores=org_dimension_scores,
            assessments=completed_audits,
            industry_type=industry_type_str,
        )
        intelligence["benchmark"] = benchmark_payload

        # 4.7 Generate dynamic narrative
        company_context = {
            "company_name": form_response.get("companyName", "the organization"),
            "industry": form_response.get(
                "industry", industry_type_str or "unspecified"
            ),
            "company_size": form_response.get("companySize", "unspecified"),
            "region": form_response.get("region", "unspecified"),
            "ai_usage_description": form_response.get("primaryAiUsage", "unspecified"),
            "governance_status": form_response.get("governanceMaturity", "unspecified"),
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
                for key in [
                    "overall_assessment",
                    "critical_risk",
                    "primary_opportunity",
                    "recommended_first_action",
                ]:
                    if key in narrative["executive_summary"]:
                        intelligence["executive_summary"][key] = narrative[
                            "executive_summary"
                        ][key]

            if "roadmap" in narrative:
                intelligence["roadmap"] = narrative["roadmap"]

            if "recommendations" in narrative:
                intelligence["recommendations"] = narrative["recommendations"]

        # 4.8 Generate and save per-system intelligence
        ai_systems = await repository.get_ai_systems_by_org(db, org_id)
        if ai_systems:
            # We must not modify the original scores_dict since it's already used
            for sys in ai_systems:
                system_context = {
                    "criticality": sys.criticality,
                    "ai_type": sys.ai_type,
                    "decision_making_role": sys.decision_making_role,
                    "data_types": sys.data_types,
                }

                # generate per-system intelligence
                sys_intel = generate_intelligence(
                    scores_dict,
                    industry_type_str,
                    form_response,
                    system_context=system_context,
                    retain_linked_finding=True,
                )

                # save to database
                await repository.create_system_finding(
                    db=db,
                    audit_id=audit.id,
                    ai_system_id=sys.id,
                    findings=sys_intel.get("findings", []),
                    recommendations=sys_intel.get("recommendations", []),
                    executive_summary=sys_intel.get("executive_summary", {}).get(
                        "overall_assessment"
                    ),
                    dimension_scores=scores_dict.get("dimensions", {}),
                )
                # create cost snapshot
                system_cost = calculate_system_cost(sys)
                await repository.create_ai_system_cost_snapshot(
                    db=db,
                    organization_id=org_id,
                    ai_system_id=sys.id,
                    audit_id=audit.id,
                    licensing_cost=sys.licensing_cost,
                    cloud_cost=sys.cloud_cost,
                    inference_cost=sys.inference_cost,
                    maintenance_cost=sys.maintenance_cost,
                    total_cost=system_cost.get("total"),
                    is_partial=system_cost.get("is_partial", False)
                )


        # Fetch per-system findings
        db_system_findings = await repository.get_system_findings_by_audit(db, audit.id)

        # We need raw dictionaries for aggregation so `linked_finding` is preserved
        raw_system_findings = [
            {
                "findings": sf.findings,
                "recommendations": sf.recommendations,
            }
            for sf in db_system_findings
        ]

        if raw_system_findings:
            aggregated_data = aggregate_top_findings_and_recommendations(raw_system_findings)
            intelligence["findings"] = aggregated_data["findings"]
            intelligence["recommendations"] = aggregated_data["recommendations"]

        system_findings_responses = [
            {
                "ai_system_id": sf.ai_system_id,
                "ai_system_name": sf.ai_system.name,
                "findings": sf.findings,
                "recommendations": sf.recommendations,
                "executive_summary": sf.executive_summary,
                "dimension_scores": sf.dimension_scores,
            }
            for sf in db_system_findings
        ]

        # Ensure linked_finding does not leak to the frontend in system_findings_responses
        for sf_resp in system_findings_responses:
            for rec in sf_resp.get("recommendations", []):
                if "linked_finding" in rec:
                    rec.pop("linked_finding", None)

        # Overwrite roadmap with per-system synthesized roadmap
        ai_system_ids = [sf.ai_system_id for sf in db_system_findings]
        db_risk_classifications = await repository.get_risk_classifications_by_audit(
            db, audit.id
        )
        db_monitoring_plans = await repository.get_monitoring_plans_by_systems(
            db, ai_system_ids
        )

        risk_class_map = {
            str(rc.ai_system_id): rc.risk_level for rc in db_risk_classifications
        }
        monitoring_plan_map = {
            str(mp.ai_system_id): mp.review_cadence for mp in db_monitoring_plans
        }

        new_roadmap_payload = generate_system_driven_roadmap(
            system_findings_responses, risk_class_map, monitoring_plan_map
        )
        intelligence["roadmap"] = new_roadmap_payload.get("roadmap", {})

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
            missing_data_flags=scores_dict.get("missing_data_flags", []),
            intelligence=intelligence,
            narrative_source=narrative_source,
            system_findings=system_findings_responses,
            status=audit.status,
            industry_type=audit.industry_type,
            created_at=audit.created_at,
        )

    except Exception as e:
        # Update status to failed if something goes wrong
        audit.status = repository.AuditStatus.failed
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit failed: {str(e)}",
        )


async def update_system_finding(
    db: AsyncSession,
    audit_id: uuid.UUID,
    org_id: uuid.UUID,
    system_finding_id: uuid.UUID,
    finding_title: str,
    update_data: Dict[str, Any]
):
    # Verify the audit belongs to the org
    await repository.get_audit(db, audit_id, org_id)

    # Update the finding
    updated_system_finding = await repository.update_system_finding_finding(
        db, audit_id, system_finding_id, finding_title, update_data
    )

    return updated_system_finding
