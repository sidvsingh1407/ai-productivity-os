import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal

class AISystemBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the AI System")
    purpose: Optional[str] = None
    data_types: List[str] = Field(default_factory=list, description="List of data types processed by the AI system")
    decision_making_role: str = Field(
        default="not_specified",
        min_length=1,
        max_length=255,
        description="Description of how the system participates in decision-making"
    )
    status: Literal['active', 'inactive', 'archived'] = Field(default='active')

    version: Optional[str] = None
    lifecycle_status: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    business_capability: Optional[str] = None
    internal_external_users: Optional[str] = None
    criticality: Optional[str] = None
    implementation_stage: Optional[str] = None
    ai_type: Optional[str] = None
    vendor: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    api_provider: Optional[str] = None
    framework: Optional[str] = None
    hosting: Optional[str] = None
    integrations: Optional[List[str]] = Field(default_factory=list)
    authentication_method: Optional[str] = None
    vector_db: Optional[str] = None
    knowledge_sources: Optional[List[str]] = Field(default_factory=list)
    workflow_engine: Optional[str] = None
    agent_framework: Optional[str] = None
    deployment_type: Optional[str] = None
    data_flow: Optional[str] = None
    apis: Optional[List[str]] = None
    databases: Optional[List[str]] = None
    event_systems: Optional[str] = None
    caching: Optional[str] = None
    monitoring: Optional[str] = None
    logging: Optional[str] = None
    deployment_details: Optional[str] = None
    data_sensitivity: Optional[str] = None
    data_sources: Optional[List[str]] = None
    data_destinations: Optional[List[str]] = None
    usage_frequency: Optional[str] = None
    users_count: Optional[int] = None
    uptime: Optional[float] = None
    approvals_required: Optional[bool] = None
    risk_classification: Optional[str] = None
    oversight_status: Optional[str] = None
    documentation_status: Optional[str] = None
    applicable_policies: Optional[List[str]] = Field(default_factory=list)
    rbac_enabled: Optional[bool] = None
    encryption_status: Optional[str] = None
    incident_count: Optional[int] = 0
    applicable_regulations: Optional[List[str]] = Field(default_factory=list)
    obligations: Optional[List[str]] = Field(default_factory=list)
    evidence_status: Optional[str] = None
    cost: Optional[float] = None
    roi_notes: Optional[str] = None
    licensing_type: Optional[str] = None
    planned_changes: Optional[str] = None
    roadmap_notes: Optional[str] = None

class AISystemCreate(AISystemBase):
    pass

class AISystemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    purpose: Optional[str] = None
    data_types: Optional[List[str]] = None
    decision_making_role: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[Literal['active', 'inactive', 'archived']] = None

    version: Optional[str] = None
    lifecycle_status: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    business_capability: Optional[str] = None
    internal_external_users: Optional[str] = None
    criticality: Optional[str] = None
    implementation_stage: Optional[str] = None
    ai_type: Optional[str] = None
    vendor: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    api_provider: Optional[str] = None
    framework: Optional[str] = None
    hosting: Optional[str] = None
    integrations: Optional[List[str]] = Field(default_factory=list)
    authentication_method: Optional[str] = None
    vector_db: Optional[str] = None
    knowledge_sources: Optional[List[str]] = Field(default_factory=list)
    workflow_engine: Optional[str] = None
    agent_framework: Optional[str] = None
    deployment_type: Optional[str] = None
    data_flow: Optional[str] = None
    apis: Optional[List[str]] = None
    databases: Optional[List[str]] = None
    event_systems: Optional[str] = None
    caching: Optional[str] = None
    monitoring: Optional[str] = None
    logging: Optional[str] = None
    deployment_details: Optional[str] = None
    data_sensitivity: Optional[str] = None
    data_sources: Optional[List[str]] = None
    data_destinations: Optional[List[str]] = None
    usage_frequency: Optional[str] = None
    users_count: Optional[int] = None
    uptime: Optional[float] = None
    approvals_required: Optional[bool] = None
    risk_classification: Optional[str] = None
    oversight_status: Optional[str] = None
    documentation_status: Optional[str] = None
    applicable_policies: Optional[List[str]] = Field(default_factory=list)
    rbac_enabled: Optional[bool] = None
    encryption_status: Optional[str] = None
    incident_count: Optional[int] = 0
    applicable_regulations: Optional[List[str]] = None
    obligations: Optional[List[str]] = None
    evidence_status: Optional[str] = None
    cost: Optional[float] = None
    roi_notes: Optional[str] = None
    licensing_type: Optional[str] = None
    planned_changes: Optional[str] = None
    roadmap_notes: Optional[str] = None

class AISystemResponse(AISystemBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AISystemListResponse(AISystemBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
