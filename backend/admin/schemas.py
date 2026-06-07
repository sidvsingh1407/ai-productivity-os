from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class OrgInfo(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    is_superadmin: bool
    is_active: bool
    organization: Optional[OrgInfo] = None
    role: str

    class Config:
        from_attributes = True

class OrgResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    member_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class SystemStatsResponse(BaseModel):
    total_users: int
    total_orgs: int
    total_audits: int
    total_workflows: int
    audits_this_month: int

class LeadResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    company: Optional[str] = None
    interest: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class LeadPaginatedResponse(BaseModel):
    items: list[LeadResponse]
    total_count: int


class UserPaginatedResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    pages: int

class OrgPaginatedResponse(BaseModel):
    items: list[OrgResponse]
    total: int
    page: int
    pages: int
