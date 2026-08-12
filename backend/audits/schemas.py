from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict, model_validator
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
    lifecycle_stage: Optional[str] = None
    ethical_dimension: Optional[str] = None

class FindingPatchUpdate(BaseModel):
    lifecycle_stage: Optional[str] = None
    ethical_dimension: Optional[str] = None

    @model_validator(mode='after')
    def check_at_least_one_field(self) -> 'FindingPatchUpdate':
        if self.lifecycle_stage is None and self.ethical_dimension is None:
            raise ValueError('At least one of lifecycle_stage or ethical_dimension must be provided.')
        return self

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
    risk_trend: str
    confidence: int
    explanation: str
    risk_drivers: List[str]
    risk_timeline: RiskTimeline

class CostOfInaction(BaseModel):
    risk_category: str
    current_risk: int
    projected_12m_risk: int
    risk_change: str
    expected_impact: List[str]
    related_recommendation: str

class EarlyWarning(BaseModel):
    warning: str
    severity: str
    suggested_action: str

class ScenarioOutcome(BaseModel):
    scenario_name: str
    expected_ohi: int
    expected_risk: int
    outcome: str
    description: str

class OperationalHealth(BaseModel):
    index: int
    explanation: str

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


class SystemFindingResponse(BaseModel):
    ai_system_id: uuid.UUID
    ai_system_name: str
    findings: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    executive_summary: Optional[str] = None
    dimension_scores: Dict[str, Any]

class AuditIntelligenceResponse(BaseModel):
    operational_health: Optional[OperationalHealth] = None
    executive_summary: ExecutiveSummary
    findings: List[Finding]
    recommendations: List[Recommendation]
    target_state: List[TargetStateItem]
    roadmap: Roadmap
    dashboard: DashboardPayload
    risk_projection: RiskProjection
    cost_of_inaction: Optional[List[CostOfInaction]] = None
    early_warnings: Optional[List[EarlyWarning]] = None
    scenario_analysis: Optional[Dict[str, ScenarioOutcome]] = None
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
    narrative_source: Optional[str] = None
    system_findings: List[SystemFindingResponse] = []

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
