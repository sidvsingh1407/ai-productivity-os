import uuid
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException, status

from models.monitoring_plan import MonitoringPlan
from models.monitoring_check_result import MonitoringCheckResult
from models.audit import Audit, AuditStatus
from models.ai_system import AISystem
from audits.intelligence_engine import generate_intelligence

async def list_monitoring_plans(db: AsyncSession, org_id: uuid.UUID, skip: int = 0, limit: int = 50) -> List[MonitoringPlan]:
    stmt = select(MonitoringPlan).where(MonitoringPlan.organization_id == org_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_monitoring_plan(db: AsyncSession, plan_id: uuid.UUID, org_id: uuid.UUID) -> MonitoringPlan:
    stmt = select(MonitoringPlan).where(MonitoringPlan.id == plan_id, MonitoringPlan.organization_id == org_id)
    result = await db.execute(stmt)
    plan = result.scalar_one_or_none()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring plan not found"
        )
    return plan

def _calculate_next_run_at(cadence: str, from_date: datetime) -> datetime:
    """Calculates the next run date based on cadence string."""
    if not cadence:
        # Default to daily if something goes wrong, though typically shouldn't happen
        return from_date + timedelta(days=1)

    cadence = cadence.lower()
    if cadence == "daily":
        return from_date + timedelta(days=1)
    elif cadence == "weekly":
        return from_date + timedelta(weeks=1)
    elif cadence == "monthly":
        return from_date + timedelta(days=30)
    elif cadence == "quarterly":
        return from_date + timedelta(days=90)
    elif cadence == "annually" or cadence == "yearly":
        return from_date + timedelta(days=365)
    else:
        # Fallback default
        return from_date + timedelta(days=1)

def _determine_overall_severity(findings: List[Dict[str, Any]]) -> str:
    """Determine the highest severity from a list of findings."""
    severity_rank = {
        "Critical": 4,
        "Major": 3,
        "Moderate": 2,
        "Advisory": 1
    }

    max_rank = 0
    max_severity = "Advisory"

    for finding in findings:
        severity = finding.get("severity")
        if severity and severity in severity_rank:
            if severity_rank[severity] > max_rank:
                max_rank = severity_rank[severity]
                max_severity = severity

    return max_severity

async def run_due_monitoring_checks(session_maker: async_sessionmaker[AsyncSession]):
    """
    Background task to scan for due monitoring plans and execute checks.
    Uses an isolated session maker since it runs in a background context.
    """
    async with session_maker() as db:
        try:
            now = datetime.now(timezone.utc)

            # Find plans due for execution (next_run_at is in the past or null but active)
            # We assume active plans without a next_run_at should run now.
            stmt = select(MonitoringPlan).where(
                MonitoringPlan.status == 'active',
                (MonitoringPlan.next_run_at <= now) | (MonitoringPlan.next_run_at.is_(None))
            )
            result = await db.execute(stmt)
            due_plans = result.scalars().all()

            for plan in due_plans:
                # 1. Fetch latest audit for this AI system to use its scores as a base
                audit_stmt = select(Audit).where(
                    Audit.status == AuditStatus.complete,
                    Audit.org_id == plan.organization_id
                    # Note: Audits are scoped to orgs. We need the audit that evaluated this AI system.
                    # SystemFindings link the two.
                ).order_by(Audit.created_at.desc()).limit(1)

                audit_result = await db.execute(audit_stmt)
                latest_audit = audit_result.scalar_one_or_none()

                if not latest_audit:
                    # Skip if no audit exists to provide base data
                    continue

                # Get the AI system to provide context
                system_stmt = select(AISystem).where(AISystem.id == plan.ai_system_id)
                system_result = await db.execute(system_stmt)
                ai_system = system_result.scalar_one_or_none()

                if not ai_system:
                    continue

                # Make sure we don't nest dimensions
                scores_dict = {"dimensions": latest_audit.scores or {}}
                if "dimensions" in scores_dict["dimensions"]:
                    scores_dict["dimensions"] = scores_dict["dimensions"]["dimensions"]

                system_context = {
                    "criticality": ai_system.criticality,
                    "ai_type": ai_system.ai_type,
                    "decision_making_role": ai_system.decision_making_role,
                    "data_types": ai_system.data_types,
                }

                # 2. Run the intelligence engine to generate findings
                industry_type_str = latest_audit.industry_type.value if hasattr(latest_audit.industry_type, 'value') else latest_audit.industry_type
                sys_intel = generate_intelligence(
                    scores_dict,
                    industry_type_str,
                    latest_audit.form_response,
                    system_context=system_context
                )

                generated_findings = sys_intel.get("findings", [])

                # 3. Create a new MonitoringCheckResult
                overall_severity = _determine_overall_severity(generated_findings)

                check_result = MonitoringCheckResult(
                    monitoring_plan_id=plan.id,
                    ai_system_id=ai_system.id,
                    findings=generated_findings,
                    severity=overall_severity
                )
                db.add(check_result)

                # 4. Update the plan's timestamps
                plan.last_reviewed_at = now
                plan.next_run_at = _calculate_next_run_at(plan.review_cadence, now)

            await db.commit()

        except Exception as e:
            await db.rollback()
            # In a production app, we would log this properly
            print(f"Error in background monitoring check: {e}")
            raise e
