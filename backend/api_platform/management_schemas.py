from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
import uuid
from models.api_platform import ApiTier

class ApiKeyCreate(BaseModel):
    name: str

class ApiKeyResponse(BaseModel):
    id: uuid.UUID
    name: str
    tier: ApiTier
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class ApiKeyCreateResponse(BaseModel):
    api_key: ApiKeyResponse
    raw_key: str

class ApiUsageLogResponse(BaseModel):
    id: uuid.UUID
    api_key_id: uuid.UUID
    endpoint: str
    request_method: str
    response_status: int
    latency_ms: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
