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

class AISystemCreate(AISystemBase):
    pass

class AISystemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    purpose: Optional[str] = None
    data_types: Optional[List[str]] = None
    decision_making_role: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[Literal['active', 'inactive', 'archived']] = None

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
