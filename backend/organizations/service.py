import re
import uuid
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization, OrgMember, OrgRole, Invitation
from organizations.repository import OrganizationRepository
from users.repository import UserRepository
from organizations.schemas import OrgResponse
from models.workflow import Workflow, WorkflowStatus
from models.engineering_record import EngineeringRecord
from sqlalchemy.future import select
from engineering.service import EngineeringRecordsService

class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.session = session
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

    async def get_operational_score(self, org_id: uuid.UUID) -> dict:
        # 1. Fetch Workflows
        stmt_wf = select(Workflow).where(
            Workflow.org_id == org_id,
            Workflow.status == WorkflowStatus.complete
        )
        result_wf = await self.session.execute(stmt_wf)
        workflows = result_wf.scalars().all()

        workflow_health_scores = []
        for wf in workflows:
            if wf.scores and 'health' in wf.scores:
                workflow_health_scores.append(wf.scores['health'])

        avg_workflow_health = None
        if workflow_health_scores:
            avg_workflow_health = sum(workflow_health_scores) / len(workflow_health_scores)

        # 2. Fetch Engineering Record
        stmt_eng = select(EngineeringRecord).where(
            EngineeringRecord.organization_id == org_id
        )
        result_eng = await self.session.execute(stmt_eng)
        engineering_record = result_eng.scalar_one_or_none()

        engineering_score = None
        if engineering_record:
            # We instantiate the service to dynamically compute the score
            eng_service = EngineeringRecordsService()
            engineering_score = eng_service._calculate_score(engineering_record)

        # 3. Combine scores
        is_partial = False
        missing_components = []
        operational_score = None
        unavailable_reason = None

        if avg_workflow_health is not None and engineering_score is not None:
            # Both present, 50/50 weighting
            operational_score = (avg_workflow_health * 0.5) + (engineering_score * 0.5)
        elif avg_workflow_health is not None:
            # Only workflow data
            operational_score = avg_workflow_health
            is_partial = True
            missing_components.append("engineering_score")
        elif engineering_score is not None:
            # Only engineering data
            operational_score = engineering_score
            is_partial = True
            missing_components.append("workflow_health_score")
        else:
            # Neither present
            is_partial = True
            missing_components = ["workflow_health_score", "engineering_score"]
            unavailable_reason = "No Workflow or Engineering Intelligence records found for this organization."

        return {
            "operational_score": operational_score,
            "is_partial": is_partial,
            "missing_components": missing_components,
            "score_unavailable_reason": unavailable_reason
        }

    async def get_org_with_operational_score(self, org: Organization) -> OrgResponse:
        score_data = await self.get_operational_score(org.id)

        return OrgResponse(
            id=org.id,
            name=org.name,
            slug=org.slug,
            created_at=org.created_at,
            updated_at=org.updated_at,
            operational_score=score_data["operational_score"],
            is_partial=score_data["is_partial"],
            missing_components=score_data["missing_components"],
            score_unavailable_reason=score_data["score_unavailable_reason"]
        )
