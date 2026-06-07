from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import uuid
from typing import List

from database import get_db
from dependencies import get_current_user, get_current_org, require_role
from models.user import User
from models.organization import Organization
from models.api_platform import ApiKey, ApiUsageLog, ApiTier
from .service import ApiKeyService
from .management_schemas import ApiKeyCreate, ApiKeyResponse, ApiKeyCreateResponse, ApiUsageLogResponse

router = APIRouter(tags=["API Platform Management"])

@router.post("/keys", response_model=ApiKeyCreateResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_api_key(
    request: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    api_key, raw_key = await ApiKeyService.create_api_key(
        db=db,
        organization_id=org.id,
        name=request.name,
        tier=ApiTier.free,  # Default tier
    )
    return ApiKeyCreateResponse(
        api_key=ApiKeyResponse.model_validate(api_key),
        raw_key=raw_key
    )

@router.get("/keys", response_model=List[ApiKeyResponse], dependencies=[Depends(require_role("admin"))])
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    query = select(ApiKey).where(
        ApiKey.organization_id == org.id,
        ApiKey.is_active == True
    ).order_by(desc(ApiKey.created_at))
    result = await db.execute(query)
    keys = result.scalars().all()
    return [ApiKeyResponse.model_validate(k) for k in keys]

@router.delete("/keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def revoke_api_key(
    key_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    # Verify the key belongs to the org before revoking
    query = select(ApiKey).where(ApiKey.id == key_id, ApiKey.organization_id == org.id)
    result = await db.execute(query)
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")

    await ApiKeyService.revoke_key(db, key_id)

@router.get("/usage", response_model=List[ApiUsageLogResponse], dependencies=[Depends(require_role("admin"))])
async def list_api_usage(
    db: AsyncSession = Depends(get_db),
    org: Organization = Depends(get_current_org)
):
    # First get org's keys
    keys_query = select(ApiKey.id).where(ApiKey.organization_id == org.id)
    keys_result = await db.execute(keys_query)
    org_key_ids = [k for k in keys_result.scalars().all()]

    if not org_key_ids:
        return []

    # Then get logs for those keys
    query = select(ApiUsageLog).where(
        ApiUsageLog.api_key_id.in_(org_key_ids)
    ).order_by(desc(ApiUsageLog.created_at)).limit(100)

    result = await db.execute(query)
    logs = result.scalars().all()
    return [ApiUsageLogResponse.model_validate(l) for l in logs]
