from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    is_superadmin: bool
    is_active: bool

    class Config:
        from_attributes = True

class OrgResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str

    class Config:
        from_attributes = True

class SystemStatsResponse(BaseModel):
    total_users: int
    total_orgs: int
    total_audits: int
    total_workflows: int
    audits_this_month: int
