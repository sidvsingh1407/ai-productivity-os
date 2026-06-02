from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from models.audit import AuditStatus

class AuditCreate(BaseModel):
    form_response: Dict[str, Any]

class AuditResponse(BaseModel):
    id: uuid.UUID
    org_id: uuid.UUID
    user_id: uuid.UUID
    form_response: Optional[Dict[str, Any]] = None
    scores: Optional[Dict[str, Any]] = None
    total_score: Optional[int] = None
    rating: Optional[str] = None
    compliance_risk_flag: Optional[bool] = None
    compliance_risk_reasons: Optional[List[str]] = None
    contradictions: Optional[List[str]] = None
    missing_data_flags: Optional[List[str]] = None
    status: AuditStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AuditListResponse(BaseModel):
    items: List[AuditResponse]
    total: int
    skip: int
    limit: int

class AuditVersionResponse(BaseModel):
    id: uuid.UUID
    audit_id: uuid.UUID
    version_number: int
    scores_snapshot: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
