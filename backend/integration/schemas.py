from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class IntegrationRequest(BaseModel):
    audit_id: UUID
    workflow_id: UUID

class RecommendationItem(BaseModel):
    blueprint_id: UUID
    priority: str
    rationale: str
    compliance_flagged: bool
    dimension: str

class IntegrationResultResponse(BaseModel):
    id: UUID
    audit_id: UUID
    workflow_id: UUID
    audit_score_summary: Dict[str, Any]
    recommendations: List[RecommendationItem]
    created_at: datetime

    class Config:
        from_attributes = True
