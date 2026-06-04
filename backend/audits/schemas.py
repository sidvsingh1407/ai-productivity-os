from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from models.audit import AuditStatus

class AuditCreate(BaseModel):
    form_response: Dict[str, Any]
    evidence_response: Optional[Dict[str, Any]] = None

class Finding(BaseModel):
    title: str
    severity: str
    impact: str
    rationale: str

class Recommendation(BaseModel):
    recommendation: str
    priority: str
    expected_impact: str
    implementation_effort: str

class ExecutiveSummary(BaseModel):
    overall_assessment: str
    critical_risk: str
    primary_opportunity: str
    recommended_first_action: str

class TargetStateItem(BaseModel):
    dimension: str
    current_score: int
    target_score: int
    gap: int
    improvement_priority: str
    rationale: str

class RoadmapAction(BaseModel):
    action: str
    reason: str
    priority: str

class Roadmap(BaseModel):
    day_30: List[RoadmapAction]
    day_60: List[RoadmapAction]
    day_90: List[RoadmapAction]

class DashboardPayload(BaseModel):
    critical_risk: str
    priority_action: str
    improvement_opportunity: str
    executive_summary: str

class RiskTimeline(BaseModel):
    near_term: List[str]
    mid_term: List[str]
    long_term: List[str]

class RiskProjection(BaseModel):
    risk_level: str
    risk_score: int
    confidence: int
    risk_drivers: List[str]
    cost_of_inaction: List[str]
    risk_timeline: RiskTimeline

class AuditIntelligenceResponse(BaseModel):
    executive_summary: ExecutiveSummary
    findings: List[Finding]
    recommendations: List[Recommendation]
    target_state: List[TargetStateItem]
    roadmap: Roadmap
    dashboard: DashboardPayload
    risk_projection: RiskProjection

class AuditResponse(BaseModel):
    id: uuid.UUID
    org_id: uuid.UUID
    user_id: uuid.UUID
    form_response: Optional[Dict[str, Any]] = None
    evidence_response: Optional[Dict[str, Any]] = None
    scores: Optional[Dict[str, Any]] = None
    total_score: Optional[int] = None
    evidence_quality_score: Optional[int] = None
    confidence_index: Optional[int] = None
    rating: Optional[str] = None
    compliance_risk_flag: Optional[bool] = None
    compliance_risk_reasons: Optional[List[str]] = None
    contradictions: Optional[List[str]] = None
    missing_data_flags: Optional[List[str]] = None

    # Consolidated Intelligence Payload
    intelligence: Optional[AuditIntelligenceResponse] = None

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
