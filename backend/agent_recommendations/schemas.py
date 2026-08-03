from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

AgentType = Literal[
    'hr_agent',
    'sales_agent',
    'legal_agent',
    'finance_agent',
    'procurement_agent',
    'customer_support_agent',
    'knowledge_agent',
    'executive_agent'
]

ConfidenceLevel = Literal['High', 'Medium', 'Low']

class AgentRecommendationBase(BaseModel):
    agent_type: AgentType
    rationale: str
    confidence: ConfidenceLevel

class AgentRecommendationCreate(AgentRecommendationBase):
    organization_id: UUID
    opportunity_id: UUID

class AgentRecommendationResponse(AgentRecommendationBase):
    id: UUID
    organization_id: UUID
    opportunity_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AgentRecommendationListResponse(BaseModel):
    items: list[AgentRecommendationResponse]
    total: int
    skip: int
    limit: int
