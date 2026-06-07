from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from models.audit import IndustryType
import uuid

class AuditApiRequest(BaseModel):
    form_response: Dict[str, Any]
    evidence_response: Optional[Dict[str, Any]] = None
    industry_type: Optional[IndustryType] = None

class RiskApiRequest(BaseModel):
    audit_id: uuid.UUID
