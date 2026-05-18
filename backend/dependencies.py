from fastapi import Depends, HTTPException
from typing import Dict, Any

# TEMP AUTH PLACEHOLDER — replace with Phase 2 auth system

async def get_current_user() -> Dict[str, Any]:
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "is_superadmin": True
    }

async def get_current_org() -> Dict[str, Any]:
    return {
        "id": "00000000-0000-0000-0000-000000000002"
    }

async def require_superadmin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    if not current_user.get("is_superadmin"):
        raise HTTPException(status_code=403, detail="Superadmin access required")
    return current_user
