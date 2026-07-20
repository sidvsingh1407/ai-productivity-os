from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_user, get_current_org
from models.user import User
from models.organization import Organization
from regulation.schemas import SearchRequest, SearchResponseItem
from regulation.service import RegulationService

router = APIRouter(tags=["Regulation"])
service = RegulationService()

@router.post("/search", response_model=List[SearchResponseItem], status_code=status.HTTP_200_OK)
async def search_regulation(
    request: SearchRequest,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """
    Search the EU AI Act grounding layer for relevant chunks based on a query.
    """
    return await service.search(db, request)
