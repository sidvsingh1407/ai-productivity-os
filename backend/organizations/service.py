import re
import uuid
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization, OrgMember, OrgRole, Invitation
from organizations.repository import OrganizationRepository
from users.repository import UserRepository

class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.repository = OrganizationRepository(session)
        self.user_repository = UserRepository(session)

    def _generate_slug(self, name: str) -> str:
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s-]+', '-', slug).strip('-')
        return slug

    async def create_organization(self, name: str) -> Organization:
        slug = self._generate_slug(name)
        org = Organization(name=name, slug=slug)
        return await self.repository.create(org)

    async def add_user_to_org(self, user_id: uuid.UUID, org_id: uuid.UUID, role: OrgRole = OrgRole.member) -> OrgMember:
        member = OrgMember(user_id=user_id, org_id=org_id, role=role)
        return await self.repository.add_member(member)

    async def get_organization(self, org_id: uuid.UUID) -> Optional[Organization]:
        return await self.repository.get_by_id(org_id)

    async def get_user_organizations(self, user_id: uuid.UUID) -> List[Organization]:
        return await self.repository.get_user_organizations(user_id)

    async def get_org_members(self, org_id: uuid.UUID) -> List[dict]:
        members = await self.repository.get_members(org_id)
        result = []
        for member in members:
            user = await self.user_repository.get_by_id(member.user_id)
            if user:
                result.append({
                    "user_id": member.user_id,
                    "org_id": member.org_id,
                    "role": member.role,
                    "joined_at": member.joined_at,
                    "user_email": user.email,
                    "user_full_name": user.full_name
                })
        return result

    async def remove_member(self, org_id: uuid.UUID, user_id: uuid.UUID) -> None:
        await self.repository.remove_member(org_id, user_id)

    async def create_invitation(self, org_id: uuid.UUID, email: str) -> Invitation:
        token = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            org_id=org_id,
            email=email,
            token=token,
            expires_at=expires_at
        )
        return await self.repository.create_invitation(invitation)

    async def get_member(self, org_id: uuid.UUID, user_id: uuid.UUID) -> Optional[OrgMember]:
        return await self.repository.get_member(org_id, user_id)
