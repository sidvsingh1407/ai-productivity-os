from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

RecommendationType = Literal[
    'automation',
    'decision_support',
    'rag',
    'ai_copilot',
    'analytics',
    'predictive_models'
]

ConfidenceLevel = Literal['High', 'Medium', 'Low']

class WorkflowRecommendationBase(BaseModel):
    recommendation_type: RecommendationType
    rationale: str
    confidence: ConfidenceLevel

class WorkflowRecommendationCreate(WorkflowRecommendationBase):
    organization_id: UUID
    opportunity_id: UUID
    agent_recommendation_id: Optional[UUID] = None

class WorkflowRecommendationResponse(WorkflowRecommendationBase):
    id: UUID
    organization_id: UUID
    opportunity_id: UUID
    agent_recommendation_id: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WorkflowRecommendationListResponse(BaseModel):
    items: list[WorkflowRecommendationResponse]
    total: int
    skip: int
    limit: int
