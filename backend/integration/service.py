import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from models.audit import Audit
from models.workflow import Workflow, IntegrationResult
from .schemas import IntegrationResultResponse
from .recommendation_engine import generate_recommendations

async def run_integration(db: AsyncSession, audit_id: uuid.UUID, workflow_id: uuid.UUID, org_id: uuid.UUID) -> IntegrationResultResponse:
    # 1. Load audit by audit_id (verify org ownership)
    stmt_audit = select(Audit).where(Audit.id == audit_id, Audit.org_id == org_id)
    result_audit = await db.execute(stmt_audit)
    audit = result_audit.scalars().first()

    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found or access denied")

    # 2. Load workflow + blueprints by workflow_id (verify org ownership)
    stmt_workflow = (
        select(Workflow)
        .options(selectinload(Workflow.blueprints))
        .where(Workflow.id == workflow_id, Workflow.org_id == org_id)
    )
    result_workflow = await db.execute(stmt_workflow)
    workflow = result_workflow.scalars().first()

    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found or access denied")

    # 3. Call recommendation engine
    recommendations = generate_recommendations(
        scores=audit.scores,
        blueprints=workflow.blueprints,
        compliance_risk_flag=audit.compliance_risk_flag
    )

    # Calculate simple audit score summary
    audit_score_summary = {
        "total_score": audit.total_score,
        "rating": audit.rating,
        "scores": audit.scores
    }

    # 4. Save to integration_results table
    integration_result = IntegrationResult(
        audit_id=audit.id,
        workflow_id=workflow.id,
        org_id=org_id,
        audit_score_summary=audit_score_summary,
        recommendations=[rec.model_dump(mode='json') for rec in recommendations]
    )

    db.add(integration_result)
    await db.commit()
    await db.refresh(integration_result)

    # 5. Return response
    return IntegrationResultResponse.model_validate(integration_result)

async def get_integration(db: AsyncSession, integration_id: uuid.UUID, org_id: uuid.UUID) -> IntegrationResultResponse:
    stmt = select(IntegrationResult).where(IntegrationResult.id == integration_id, IntegrationResult.org_id == org_id)
    result = await db.execute(stmt)
    integration = result.scalars().first()

    if not integration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration result not found or access denied")

    return IntegrationResultResponse.model_validate(integration)
