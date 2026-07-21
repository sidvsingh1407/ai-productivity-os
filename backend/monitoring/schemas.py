from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class MonitoringPlanBase(BaseModel):
    status: str
    monitoring_scope: List[Dict[str, Any]] = []
    review_cadence: Optional[str] = None

class MonitoringPlanResponse(MonitoringPlanBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    ai_system_id: uuid.UUID
    risk_classification_id: Optional[uuid.UUID] = None
    last_reviewed_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MonitoringCheckResultResponse(BaseModel):
    id: uuid.UUID
    monitoring_plan_id: uuid.UUID
    ai_system_id: uuid.UUID
    findings: List[Dict[str, Any]]
    severity: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
