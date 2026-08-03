from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

OpportunityCategory = Literal[
    'manual_work',
    'repetitive_decisions',
    'knowledge_bottleneck',
    'customer_pain',
    'department_pain',
    'automation_candidate'
]

OpportunityPriority = Literal['High', 'Medium', 'Low']

class OpportunityBase(BaseModel):
    category: OpportunityCategory
    title: str
    description: str
    source_module: str
    confidence_or_priority: OpportunityPriority

class OpportunityCreate(OpportunityBase):
    organization_id: UUID
    ai_system_id: Optional[UUID] = None

class OpportunityResponse(OpportunityBase):
    id: UUID
    organization_id: UUID
    ai_system_id: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OpportunityListResponse(BaseModel):
    items: list[OpportunityResponse]
    total: int
    skip: int
    limit: int
