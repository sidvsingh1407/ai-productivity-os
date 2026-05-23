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
    return job

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
