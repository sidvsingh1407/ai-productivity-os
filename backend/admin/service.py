from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from datetime import datetime, timezone
import uuid

from models.user import User
from models.organization import Organization
from models.audit import Audit
from models.workflow import Workflow
from models.contact import ContactLead
from admin.schemas import UserResponse, OrgResponse, LeadPaginatedResponse, LeadResponse

async def list_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserResponse]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]

async def list_all_orgs(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[OrgResponse]:
    result = await db.execute(select(Organization).offset(skip).limit(limit))
    orgs = result.scalars().all()
    return [OrgResponse.model_validate(org) for org in orgs]

async def deactivate_user(db: AsyncSession, user_id: uuid.UUID) -> UserResponse | None:
    stmt = update(User).where(User.id == user_id).values(is_active=False).returning(User)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        await db.commit()
        return UserResponse.model_validate(user)
    return None

async def get_system_stats(db: AsyncSession) -> dict:
    total_users = await db.scalar(select(func.count(User.id)))
    total_orgs = await db.scalar(select(func.count(Organization.id)))
    total_audits = await db.scalar(select(func.count(Audit.id)))
    total_workflows = await db.scalar(select(func.count(Workflow.id)))

    now = datetime.now(timezone.utc)
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    audits_this_month = await db.scalar(select(func.count(Audit.id)).where(Audit.created_at >= start_of_month))

    return {
        "total_users": total_users or 0,
        "total_orgs": total_orgs or 0,
        "total_audits": total_audits or 0,
        "total_workflows": total_workflows or 0,
        "audits_this_month": audits_this_month or 0
    }

async def list_all_leads(db: AsyncSession, skip: int = 0, limit: int = 100) -> LeadPaginatedResponse:
    total_count = await db.scalar(select(func.count(ContactLead.id)))
    result = await db.execute(
        select(ContactLead)
        .order_by(ContactLead.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    leads = result.scalars().all()
    return LeadPaginatedResponse(
        items=[LeadResponse.model_validate(lead) for lead in leads],
        total_count=total_count or 0
    )
