from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class DiagnosticStepInput(BaseModel):
    step_name: str
    owner_role: str
    requires_approval: bool = False
    system_tool: Optional[str] = None
    manual_handoff: bool = False

class WorkflowCreate(BaseModel):
    # DEPRECATED fields in input_config: organizationType, industry, department, workflowCategory, teamSize, currentToolsUsed, workflowDescription, currentChallenges
    input_config: Dict[str, Any]
    steps_input: Optional[List[DiagnosticStepInput]] = None

from uuid import UUID

class WorkflowResponse(BaseModel):
    id: UUID
    org_id: UUID
    user_id: UUID
    status: str
    input_config: Dict[str, Any]
    steps_input: Optional[List[Dict[str, Any]]] = None
    scores: Optional[Dict[str, int]] = None
    findings: Optional[Dict[str, List[str]]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BlueprintResponse(BaseModel):
    id: UUID
    workflow_id: UUID
    process_id: str
    automation_tier: str
    industry_variant: Optional[str] = None
    confidence: float
    merged: bool
    blueprint_data: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class RootCause(BaseModel):
    root_cause: str
    evidence: str
    impact: str

class Bottleneck(BaseModel):
    title: str
    severity: str
    impacted_area: str
    rationale: str
    root_cause: RootCause

class Risk(BaseModel):
    workflow_risk: str
    primary_risk: str
    rationale: str
    execution_risk: str
    delay_risk: str
    dependency_risk: str
    scalability_risk: str

class Recommendation(BaseModel):
    recommendation: str
    priority: str
    expected_impact: str
    implementation_effort: str

class ExecutiveSummary(BaseModel):
    most_critical_bottleneck: str
    primary_root_cause: str
    highest_priority_intervention: str
    workflow_risk_level: str
    workflow_maturity: str

class WorkflowIntelligence(BaseModel):
    # DEPRECATED: This entire schema and its usage is deprecated in favor of the new diagnostic engine (scores/findings).
    executive_summary: ExecutiveSummary
    workflow_maturity: str
    workflow_risk_level: str
    most_critical_bottleneck: str
    primary_root_cause: str  # DEPRECATED field
    highest_priority_intervention: str  # DEPRECATED field
    bottlenecks: List[Bottleneck]
    risks: List[Risk]  # DEPRECATED field
    recommendations: List[Recommendation]  # DEPRECATED field

class WorkflowDetailResponse(WorkflowResponse):
    blueprints: List[BlueprintResponse] = []
    intelligence: Optional[WorkflowIntelligence] = None
    narrative_source: Optional[str] = None
