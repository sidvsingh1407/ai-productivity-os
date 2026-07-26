import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal

class AdoptionRecordBase(BaseModel):
    ai_system_id: uuid.UUID = Field(..., description="ID of the associated AI System")
    department: str = Field(..., min_length=1, max_length=255, description="Department using the AI System")
    user_count: int = Field(default=0, description="Number of users in the department")
    usage_frequency: Literal['daily', 'weekly', 'monthly', 'rare', 'not_specified'] = Field(default='not_specified')
    shadow_ai_detected: bool = Field(default=False)
    champions: List[str] = Field(default_factory=list, max_length=20, description="List of champions for the AI system in this department")
    resistance_level: Literal['low', 'medium', 'high', 'not_specified'] = Field(default='not_specified')
    training_status: Literal['none', 'planned', 'in_progress', 'completed', 'not_specified'] = Field(default='not_specified')

class AdoptionRecordCreate(AdoptionRecordBase):
    pass

class AdoptionRecordUpdate(BaseModel):
    # Do not allow updating ai_system_id or department since they are part of the unique constraint
    # (If they need to change those, they should delete and recreate, or we can revisit this later)
    user_count: Optional[int] = None
    usage_frequency: Optional[Literal['daily', 'weekly', 'monthly', 'rare', 'not_specified']] = None
    shadow_ai_detected: Optional[bool] = None
    champions: Optional[List[str]] = Field(None, max_length=20)
    resistance_level: Optional[Literal['low', 'medium', 'high', 'not_specified']] = None
    training_status: Optional[Literal['none', 'planned', 'in_progress', 'completed', 'not_specified']] = None

class AdoptionRecordResponse(AdoptionRecordBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    adoption_score: float = Field(default=0.0, description="Dynamically calculated score 0-100")

    model_config = ConfigDict(from_attributes=True)

class AdoptionRecordListResponse(AdoptionRecordBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    adoption_score: float = Field(default=0.0, description="Dynamically calculated score 0-100")

    model_config = ConfigDict(from_attributes=True)
