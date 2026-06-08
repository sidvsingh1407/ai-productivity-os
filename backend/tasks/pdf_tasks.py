import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import async_session_maker
from models.audit import Audit
from models.workflow import IntegrationResult
from models.report import ExportJob, Report, ExportJobStatus
from tasks.celery_app import celery_app
from reports.pdf_generator import generate_audit_pdf
from audits.intelligence_engine import generate_intelligence

async def _generate_pdf_async(audit_id: str, org_id: str):
    async with async_session_maker() as session:
        # 1. Load audit from DB
        audit = await session.get(Audit, audit_id)
        if not audit:
            raise ValueError(f"Audit {audit_id} not found")

        # Optional: ensure audit matches org_id
        if str(audit.org_id) != org_id:
            raise ValueError("Audit does not belong to the organization")

        # 2. Reconstruct scores_dict to generate intelligence
        scores_dict = {
            'dimensions': audit.scores or {},
            'compliance_risk_flag': audit.compliance_risk_flag,
            'compliance_risk_reasons': audit.compliance_risk_reasons or [],
            'contradictions': audit.contradictions or [],
            'missing_data_flags': []
        }

        # 3. Generate Intelligence Package
        intelligence = generate_intelligence(scores_dict)

        # Prepare data for PDF generator
        audit_data = {
            "company_name": "Organization Data", # Ideally we'd fetch the Org name, but keeping it simple based on spec
            "scores": audit.scores or {},
            "total_score": audit.total_score,
            "rating": audit.rating,
            "compliance_risk_flag": audit.compliance_risk_flag,
            "compliance_risk_reasons": audit.compliance_risk_reasons or [],
            "intelligence": intelligence
        }

        # Output path
        output_dir = os.path.join("backend", "storage", "reports", str(org_id))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{audit_id}.pdf")

        # 3. Call pdf generator
        file_path = generate_audit_pdf(audit_data, output_path)

        # 5. Create report record in DB
        file_size = os.path.getsize(file_path)
        report = Report(
            audit_id=audit_id,
            file_path=file_path,
            file_size=file_size
        )
        session.add(report)

        # 6. Update export_job status to complete
        stmt_job = select(ExportJob).where(
            ExportJob.audit_id == audit_id,
            ExportJob.status == ExportJobStatus.pending
        )
        job_result = await session.execute(stmt_job)
        jobs = job_result.scalars().all()
        for job in jobs:
            job.status = ExportJobStatus.complete
            job.result_path = file_path

        await session.commit()
        return file_path

@celery_app.task(name="backend.tasks.pdf_tasks.generate_pdf_task")
def generate_pdf_task(audit_id: str, org_id: str):
    # Run the async flow in an event loop using asyncio.run
    return asyncio.run(_generate_pdf_async(audit_id, org_id))
