from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from users.repository import UserRepository
from users.schemas import UserCreate
from auth.password_utils import hash_password

class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)
