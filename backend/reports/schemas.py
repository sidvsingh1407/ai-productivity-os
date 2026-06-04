from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from models.report import ExportJobStatus, ExportJobType

class ExportJobResponse(BaseModel):
    id: UUID
    user_id: UUID
    org_id: UUID
    audit_id: UUID
    job_type: ExportJobType
    status: ExportJobStatus
    result_path: Optional[str] = None
    download_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReportResponse(BaseModel):
    id: UUID
    audit_id: UUID
    file_path: str
    file_size: int
    generated_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True
