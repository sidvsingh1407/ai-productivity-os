import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from models.audit import Audit, AuditVersion, AuditStatus
from models.ai_system import AISystem
from models.system_finding import SystemFinding
from models.risk_classification import RiskClassification
from models.monitoring_plan import MonitoringPlan


async def create_audit(
    db: AsyncSession,
    org_id: uuid.UUID,
    user_id: uuid.UUID,
    form_response: Dict[str, Any],
    evidence_response: Optional[Dict[str, Any]] = None,
    industry_type: Optional[str] = None,
) -> Audit:
    db_audit = Audit(
        org_id=org_id,
        user_id=user_id,
        form_response=form_response,
        evidence_response=evidence_response,
        industry_type=industry_type,
        status=AuditStatus.running,
    )
    db.add(db_audit)
    await db.commit()
    await db.refresh(db_audit)
    return db_audit


async def get_audit(db: AsyncSession, audit_id: uuid.UUID, org_id: uuid.UUID) -> Audit:
    stmt = select(Audit).where(Audit.id == audit_id, Audit.org_id == org_id)
    result = await db.execute(stmt)
    db_audit = result.scalar_one_or_none()

    if not db_audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found"
        )
    return db_audit


async def list_audits(
    db: AsyncSession, org_id: uuid.UUID, skip: int = 0, limit: int = 20
) -> List[Audit]:
    stmt = select(Audit).where(Audit.org_id == org_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_total_audits(db: AsyncSession, org_id: uuid.UUID) -> int:
    stmt = select(Audit).where(Audit.org_id == org_id)
    result = await db.execute(stmt)
    return len(result.scalars().all())  # not very optimal but sufficient for now


async def save_audit_scores(
    db: AsyncSession, audit_id: uuid.UUID, scores_dict: Dict[str, Any]
) -> Audit:
    stmt = select(Audit).where(Audit.id == audit_id)
    result = await db.execute(stmt)
    db_audit = result.scalar_one_or_none()

    if not db_audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found"
        )

    db_audit.scores = scores_dict.get("dimensions", {})
    db_audit.total_score = scores_dict.get("total_score")
    db_audit.rating = scores_dict.get("rating")
    db_audit.evidence_quality_score = scores_dict.get("evidence_quality_score")
    db_audit.confidence_index = scores_dict.get("confidence_index")
    db_audit.contradictions = scores_dict.get("contradictions", [])
    db_audit.compliance_risk_flag = scores_dict.get("compliance_risk_flag")
    db_audit.compliance_risk_reasons = scores_dict.get("compliance_risk_reasons")
    db_audit.status = AuditStatus.complete

    await db.commit()
    await db.refresh(db_audit)
    return db_audit


async def create_audit_version(
    db: AsyncSession,
    audit_id: uuid.UUID,
    version_number: int,
    scores_snapshot: Dict[str, Any],
) -> AuditVersion:
    db_version = AuditVersion(
        audit_id=audit_id,
        version_number=version_number,
        scores_snapshot=scores_snapshot,
    )
    db.add(db_version)
    await db.commit()
    await db.refresh(db_version)
    return db_version


async def list_audit_versions(
    db: AsyncSession, audit_id: uuid.UUID
) -> List[AuditVersion]:
    stmt = (
        select(AuditVersion)
        .where(AuditVersion.audit_id == audit_id)
        .order_by(AuditVersion.version_number.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_all_completed_audits(db: AsyncSession) -> List[Audit]:
    stmt = select(Audit).where(Audit.status == AuditStatus.complete)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_ai_systems_by_org(db: AsyncSession, org_id: uuid.UUID) -> List[AISystem]:
    stmt = select(AISystem).where(AISystem.organization_id == org_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_system_finding(
    db: AsyncSession,
    audit_id: uuid.UUID,
    ai_system_id: uuid.UUID,
    findings: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]],
    executive_summary: Optional[str],
    dimension_scores: Dict[str, Any],
) -> SystemFinding:
    db_system_finding = SystemFinding(
        audit_id=audit_id,
        ai_system_id=ai_system_id,
        findings=findings,
        recommendations=recommendations,
        executive_summary=executive_summary,
        dimension_scores=dimension_scores,
    )
    db.add(db_system_finding)
    await db.commit()
    await db.refresh(db_system_finding)
    return db_system_finding


async def get_system_findings_by_audit(
    db: AsyncSession, audit_id: uuid.UUID
) -> List[SystemFinding]:
    stmt = (
        select(SystemFinding)
        .where(SystemFinding.audit_id == audit_id)
        .options(joinedload(SystemFinding.ai_system))
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_risk_classifications_by_audit(
    db: AsyncSession, audit_id: uuid.UUID
) -> List[RiskClassification]:
    stmt = select(RiskClassification).where(RiskClassification.audit_id == audit_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_monitoring_plans_by_systems(
    db: AsyncSession, ai_system_ids: List[uuid.UUID]
) -> List[MonitoringPlan]:
    if not ai_system_ids:
        return []
    stmt = select(MonitoringPlan).where(MonitoringPlan.ai_system_id.in_(ai_system_ids))
    result = await db.execute(stmt)
    return list(result.scalars().all())
