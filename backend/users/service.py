from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from models.organization import OrgMember, OrgRole
from models.audit import Audit
from models.workflow import Workflow
from models.report import ExportJob
from users.repository import UserRepository
from users.schemas import UserCreate
from auth.password_utils import hash_password
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def delete_account(self, user_id: UUID) -> None:
        """
        Deletes the user's account safely following data governance rules.
        """
        session = self.repository.session

        # 1. Check if user exists
        user = await self.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")

        # 2. Check organization ownership transfer requirement
        # Find all organizations the user is a member of
        stmt = select(OrgMember).where(OrgMember.user_id == user_id)
        result = await session.execute(stmt)
        memberships = result.scalars().all()

        org_ids = [m.org_id for m in memberships]

        if org_ids:
            # Check for each org if this user is the sole owner/admin
            for org_id in org_ids:
                stmt_org_admins = select(OrgMember).where(
                    OrgMember.org_id == org_id,
                    OrgMember.role.in_([OrgRole.owner, OrgRole.admin]),
                )
                result = await session.execute(stmt_org_admins)
                admins_and_owners = result.scalars().all()

                if (
                    len(admins_and_owners) == 1
                    and admins_and_owners[0].user_id == user_id
                ):
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "error": {
                                "code": "OWNER_TRANSFER_REQUIRED",
                                "message": "Transfer organization ownership before deleting account.",
                            }
                        },
                    )

        # We assume the system "Deleted User" UUID is 00000000-0000-0000-0000-000000000000
        # as set up in our migration script.
        DELETED_USER_ID = UUID("00000000-0000-0000-0000-000000000000")

        try:
            # 3. Anonymize Audits
            await session.execute(
                update(Audit)
                .where(Audit.user_id == user_id)
                .values(user_id=DELETED_USER_ID)
            )

            # 4. Anonymize Workflows
            await session.execute(
                update(Workflow)
                .where(Workflow.user_id == user_id)
                .values(user_id=DELETED_USER_ID)
            )

            # 5. Anonymize ExportJobs
            await session.execute(
                update(ExportJob)
                .where(ExportJob.user_id == user_id)
                .values(user_id=DELETED_USER_ID)
            )

            # 6. Delete OrgMemberships
            await session.execute(delete(OrgMember).where(OrgMember.user_id == user_id))

            # 7. Soft Delete User
            user.is_active = False
            user.hashed_password = ""
            user.full_name = "Deleted User"
            user.email = f"deleted_{user.id}@deleted.local"

            await session.commit()
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Transaction failed during account deletion: {str(e)}",
            )
