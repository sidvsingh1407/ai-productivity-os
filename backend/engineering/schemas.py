import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal, Dict, Any

class EngineeringRecordBase(BaseModel):
    has_dedicated_ai_team: bool = Field(default=False)
    team_size: int = Field(default=0)
    roles: List[str] = Field(default_factory=list, description="Roles in the AI team")
    consultants_used: List[Dict[str, Any]] = Field(default_factory=list, description="List of vendor dicts, e.g. {'vendor': 'X', 'engagement': 'Y'}")

    has_mlops_pipeline: bool = Field(default=False)
    monitoring_tooling: List[str] = Field(default_factory=list)

    has_dedicated_prompt_engineer: bool = Field(default=False)
    prompt_engineer_count: int = Field(default=0)

    has_dedicated_devops: bool = Field(default=False)
    devops_support_type: str = Field(default='not_specified', max_length=255)

    ai_engineering_budget: Optional[float] = None
    planned_investment_roadmap: Optional[str] = None


class EngineeringRecordCreate(EngineeringRecordBase):
    pass


class EngineeringRecordUpdate(BaseModel):
    has_dedicated_ai_team: Optional[bool] = None
    team_size: Optional[int] = None
    roles: Optional[List[str]] = None
    consultants_used: Optional[List[Dict[str, Any]]] = None

    has_mlops_pipeline: Optional[bool] = None
    monitoring_tooling: Optional[List[str]] = None

    has_dedicated_prompt_engineer: Optional[bool] = None
    prompt_engineer_count: Optional[int] = None

    has_dedicated_devops: Optional[bool] = None
    devops_support_type: Optional[str] = Field(None, max_length=255)

    ai_engineering_budget: Optional[float] = None
    planned_investment_roadmap: Optional[str] = None


class EngineeringRecordResponse(EngineeringRecordBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    engineering_score: float = Field(default=0.0, description="Dynamically calculated score 0-100")

    model_config = ConfigDict(from_attributes=True)

class EngineeringRecordListResponse(EngineeringRecordBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    engineering_score: float = Field(default=0.0, description="Dynamically calculated score 0-100")

    model_config = ConfigDict(from_attributes=True)
