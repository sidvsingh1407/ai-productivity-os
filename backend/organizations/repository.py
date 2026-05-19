from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization, OrgMember, Invitation
from models.user import User

class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, org_id: UUID) -> Optional[Organization]:
        result = await self.session.execute(select(Organization).where(Organization.id == org_id))
        return result.scalar_one_or_none()

    async def create(self, org: Organization) -> Organization:
        self.session.add(org)
        await self.session.commit()
        await self.session.refresh(org)
        return org

    async def add_member(self, member: OrgMember) -> OrgMember:
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def get_members(self, org_id: UUID) -> List[OrgMember]:
        result = await self.session.execute(
            select(OrgMember)
            .where(OrgMember.org_id == org_id)
        )
        return list(result.scalars().all())

    async def get_member(self, org_id: UUID, user_id: UUID) -> Optional[OrgMember]:
        result = await self.session.execute(
            select(OrgMember)
            .where(OrgMember.org_id == org_id, OrgMember.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def remove_member(self, org_id: UUID, user_id: UUID) -> None:
        member = await self.get_member(org_id, user_id)
        if member:
            await self.session.delete(member)
            await self.session.commit()

    async def get_user_organizations(self, user_id: UUID) -> List[Organization]:
        result = await self.session.execute(
            select(Organization)
            .join(OrgMember, OrgMember.org_id == Organization.id)
            .where(OrgMember.user_id == user_id)
        )
        return list(result.scalars().all())

    async def create_invitation(self, invitation: Invitation) -> Invitation:
        self.session.add(invitation)
        await self.session.commit()
        await self.session.refresh(invitation)
        return invitation
