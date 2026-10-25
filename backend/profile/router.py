from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from dependencies import get_current_user
from models.user import User
from profile.schemas import ProfileDraftResponse
from profile.service import ProfileParserService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/import", response_model=ProfileDraftResponse)
async def import_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        service = ProfileParserService()
        result = await service.parse_cv(file)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Failed to import CV: {e}")
        raise HTTPException(status_code=500, detail="Failed to process CV")
