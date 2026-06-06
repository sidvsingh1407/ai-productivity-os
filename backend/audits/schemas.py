from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from models.audit import AuditStatus, IndustryType

class AuditCreate(BaseModel):
    form_response: Dict[str, Any]
    evidence_response: Optional[Dict[str, Any]] = None
    industry_type: Optional[IndustryType] = None

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
    top_failure_risk: Optional[Dict[str, str]] = None

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

class FailureIntervention(BaseModel):
    intervention: str
    impact: str
    effort: str

class FailureIntelligence(BaseModel):
    pattern: str
    severity: str
    confidence: int
    why_detected: str
    root_causes: List[str]
    consequences: List[str]
    recommended_actions: List[FailureIntervention]

class BenchmarkDimension(BaseModel):
    score: float
    benchmark: int
    difference: float

class BenchmarkPayload(BaseModel):
    available: bool
    benchmark_type: str
    message: Optional[str] = None
    sample_size: Optional[int] = None
    platform_average: Optional[float] = None
    industry_average: Optional[float] = None
    industry_benchmark_available: Optional[bool] = None
    percentile_rank: Optional[int] = None
    dimension_comparisons: Optional[Dict[str, BenchmarkDimension]] = None
    insights: Optional[List[str]] = None

class AuditIntelligenceResponse(BaseModel):
    executive_summary: ExecutiveSummary
    findings: List[Finding]
    recommendations: List[Recommendation]
    target_state: List[TargetStateItem]
    roadmap: Roadmap
    dashboard: DashboardPayload
    risk_projection: RiskProjection
    failure_intelligence: Optional[List[FailureIntelligence]] = None
    benchmark: Optional[BenchmarkPayload] = None

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
    industry_type: Optional[IndustryType] = None
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
