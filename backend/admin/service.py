from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload, outerjoin
from datetime import datetime, timezone
import uuid
import math

from models.user import User
from models.organization import Organization, OrgMember
from models.audit import Audit
from models.workflow import Workflow
from models.contact import ContactLead
from admin.schemas import UserResponse, OrgResponse, LeadPaginatedResponse, LeadResponse, UserPaginatedResponse, OrgPaginatedResponse

async def list_all_users(db: AsyncSession, page: int = 1, limit: int = 100) -> UserPaginatedResponse:
    skip = (page - 1) * limit

    total_count = await db.scalar(select(func.count(User.id)))

    # First get the users for the current page
    stmt = select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()

    if not users:
        return UserPaginatedResponse(items=[], total=total_count or 0, page=page, pages=math.ceil((total_count or 0) / limit) if limit > 0 else 1)

    user_ids = [u.id for u in users]

    # Then fetch their primary organization/role
    # We fetch the first org mapping for simplicity as users typically have 1 org
    stmt_orgs = (
        select(OrgMember.user_id, OrgMember.role, Organization.name)
        .join(Organization, OrgMember.org_id == Organization.id)
        .where(OrgMember.user_id.in_(user_ids))
    )
    result_orgs = await db.execute(stmt_orgs)
    org_mappings = {}
    for user_id, role, org_name in result_orgs.all():
        if user_id not in org_mappings: # just take the first one
            org_mappings[user_id] = {"role": role.value, "org_name": org_name}

    users_data = []
    for user in users:
        name_parts = user.full_name.split(" ")
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        mapping = org_mappings.get(user.id, {})

        users_data.append(UserResponse(
            id=user.id,
            email=user.email,
            first_name=first_name,
            last_name=last_name,
            is_superadmin=user.is_superadmin,
            is_active=user.is_active,
            organization={"name": mapping.get("org_name")} if mapping.get("org_name") else None,
            role=mapping.get("role", "none")
        ))

    return UserPaginatedResponse(
        items=users_data,
        total=total_count or 0,
        page=page,
        pages=math.ceil((total_count or 0) / limit) if limit > 0 else 1
    )

async def list_all_orgs(db: AsyncSession, page: int = 1, limit: int = 100) -> OrgPaginatedResponse:
    skip = (page - 1) * limit

    total_count = await db.scalar(select(func.count(Organization.id)))

    stmt = (
        select(Organization, func.count(OrgMember.user_id).label('member_count'))
        .outerjoin(OrgMember, Organization.id == OrgMember.org_id)
        .group_by(Organization.id)
        .order_by(Organization.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()

    orgs_data = []
    for org, member_count in rows:
        orgs_data.append(OrgResponse(
            id=org.id,
            name=org.name,
            slug=org.slug,
            member_count=member_count,
            created_at=org.created_at
        ))

    return OrgPaginatedResponse(
        items=orgs_data,
        total=total_count or 0,
        page=page,
        pages=math.ceil((total_count or 0) / limit) if limit > 0 else 1
    )

async def deactivate_user(db: AsyncSession, user_id: uuid.UUID) -> UserResponse | None:
    # Need to return UserResponse matching the new schema
    stmt = update(User).where(User.id == user_id).values(is_active=False).returning(User)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        await db.commit()
        # Fetch the extra info to populate UserResponse properly
        stmt_orgs = (
            select(OrgMember.role, Organization.name)
            .join(Organization, OrgMember.org_id == Organization.id)
            .where(OrgMember.user_id == user.id)
            .limit(1)
        )
        res_orgs = await db.execute(stmt_orgs)
        org_row = res_orgs.first()

        name_parts = user.full_name.split(" ")
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=first_name,
            last_name=last_name,
            is_superadmin=user.is_superadmin,
            is_active=user.is_active,
            organization={"name": org_row.name} if org_row else None,
            role=org_row.role.value if org_row else "none"
        )
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
