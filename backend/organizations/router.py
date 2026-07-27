import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependencies import get_current_user, get_current_org, require_role
from organizations.schemas import OrgResponse, OrgMemberResponse, InviteCreate
from organizations.service import OrganizationService
from models.user import User
from models.organization import Organization

router = APIRouter(tags=["organizations"])

@router.get("/me", response_model=OrgResponse)
async def get_my_org(current_org: Organization = Depends(get_current_org), db: AsyncSession = Depends(get_db)):
    org_service = OrganizationService(db)
    return await org_service.get_org_with_operational_score(current_org)

@router.get("/members", response_model=List[OrgMemberResponse], dependencies=[Depends(require_role("admin"))])
async def list_members(current_org: Organization = Depends(get_current_org), db: AsyncSession = Depends(get_db)):
    org_service = OrganizationService(db)
    return await org_service.get_org_members(current_org.id)

@router.post("/invite", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_invite(
    invite_data: InviteCreate,
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    invitation = await org_service.create_invitation(current_org.id, invite_data.email)
    # TODO: Send email
    return {"message": "Invitation created", "token": invitation.token}

@router.delete("/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def remove_member(
    user_id: uuid.UUID,
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    # Ensure not removing oneself if only admin, etc. Simplification for now:
    await org_service.remove_member(current_org.id, user_id)
