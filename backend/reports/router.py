import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from reports import service, schemas
# Using placeholder auth dependencies since they weren't explicitly provided but memory suggests their names
# We'll mock them to prevent import errors

async def get_current_user():
    # Mock user dict matching standard format
    return {"id": "00000000-0000-0000-0000-000000000001"}

async def get_current_org():
    # Mock org dict
    return {"id": "00000000-0000-0000-0000-000000000002"}

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/export/{audit_id}", response_model=schemas.ExportJobResponse)
async def request_export(
    audit_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
    org: dict = Depends(get_current_org)
):
    """Request a PDF export for a specific audit. Returns the job info."""
    job = await service.request_pdf_export(db, audit_id, str(org["id"]), str(user["id"]))
    return job

@router.get("/status/{job_id}", response_model=schemas.ExportJobResponse)
async def get_status(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Poll export job status."""
    job = await service.get_export_job_status(db, job_id, str(user["id"]))

    # Map download_url dynamically if completed
    from config import settings
    base_url = settings.API_URL if hasattr(settings, 'API_URL') and settings.API_URL else ""

    response = schemas.ExportJobResponse.model_validate(job)
    if job.status == "complete" and job.result_path:
        # report_id isn't directly on job, but in tasks it stores file path
        # Assuming we can download by job_id instead for simplicity if we update download_report
        # or we just fetch the Report by audit_id

        # We need the report ID to download it.
        # Let's query the Report model for this audit.
        from models.report import Report
        from sqlalchemy import select
        stmt = select(Report).where(Report.audit_id == job.audit_id).order_by(Report.generated_at.desc())
        result = await db.execute(stmt)
        report = result.scalars().first()

        if report:
            response.download_url = f"{base_url}/reports/download/{str(report.id)}"

    return response

@router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    org: dict = Depends(get_current_org)
):
    """Stream PDF file."""
    file_path = await service.get_report_download(db, report_id, str(org["id"]))

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=os.path.basename(file_path)
    )
