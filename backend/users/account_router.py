from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from dependencies import get_current_user
from models.user import User
from users.service import UserService

router = APIRouter(prefix="/api/account", tags=["account"])

@router.delete("/delete")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    await user_service.delete_account(current_user.id)
    return {
        "status": "success",
        "message": "Account deleted successfully."
    }
