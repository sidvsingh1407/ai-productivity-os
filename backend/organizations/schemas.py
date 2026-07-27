from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from models.organization import OrgRole

class OrgCreate(BaseModel):
    name: str

class OrgResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    operational_score: Optional[float] = None
    is_partial: bool = False
    missing_components: List[str] = []
    score_unavailable_reason: Optional[str] = None

    readiness_score: Optional[float] = None
    readiness_is_partial: bool = False
    readiness_missing_components: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class OrgMemberResponse(BaseModel):
    user_id: UUID
    org_id: UUID
    role: OrgRole
    joined_at: datetime
    user_email: Optional[str] = None
    user_full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class InviteCreate(BaseModel):
    email: EmailStr
