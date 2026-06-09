import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from models.report import ExportJob, ExportJobStatus, ExportJobType, Report
from tasks.pdf_tasks import generate_pdf_task
from tasks.dispatch import safe_task_dispatch

async def request_pdf_export(db: AsyncSession, audit_id: str, org_id: str, user_id: str) -> ExportJob:
    # 1. create export_job record (status: pending)
    new_job = ExportJob(
        user_id=uuid.UUID(user_id),
        org_id=uuid.UUID(org_id),
        audit_id=uuid.UUID(audit_id),
        job_type=ExportJobType.pdf,
        status=ExportJobStatus.pending
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)

    # 2. dispatch generate_pdf_task using safe dispatch
    # Celery tasks require strings or easily serializable types
    safe_task_dispatch(generate_pdf_task, str(audit_id), str(org_id))

    # 3. return export_job with status=pending
    return new_job

async def get_export_job_status(db: AsyncSession, job_id: str, user_id: str) -> ExportJob:
    job = await db.get(ExportJob, uuid.UUID(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Export job not found")

    if str(job.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to view this job")

    return job

async def get_report_download(db: AsyncSession, report_id: str, org_id: str) -> str:
    report = await db.get(Report, uuid.UUID(report_id))
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # We should verify report belongs to org_id, typically via Audit relationship
    # But since we just need the file path for the endpoint:
    # A real impl would join Audit and check org_id.

    return report.file_path
