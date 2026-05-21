from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class WorkflowCreate(BaseModel):
    input_config: Dict[str, Any]

class WorkflowResponse(BaseModel):
    id: str
    org_id: str
    user_id: str
    status: str
    input_config: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BlueprintResponse(BaseModel):
    id: str
    workflow_id: str
    process_id: str
    automation_tier: str
    industry_variant: Optional[str] = None
    confidence: float
    merged: bool
    blueprint_data: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class WorkflowDetailResponse(WorkflowResponse):
    blueprints: List[BlueprintResponse] = []
