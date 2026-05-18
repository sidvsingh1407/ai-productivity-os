from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from users.repository import UserRepository
from organizations.service import OrganizationService
from auth.password_utils import hash_password, verify_password
from auth.jwt_utils import create_access_token, create_refresh_token, decode_token
from models.user import User
from models.organization import Organization, OrgMember, OrgRole

class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
        self.org_service = OrganizationService(session)

    async def register_user(self, email: str, password: str, full_name: str, org_name: str) -> dict:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        try:
            # Create user
            hashed_pwd = hash_password(password)
            new_user = User(email=email, hashed_password=hashed_pwd, full_name=full_name)
            self.user_repository.session.add(new_user)
            await self.user_repository.session.flush()

            # Create organization
            slug = self.org_service._generate_slug(org_name)
            org = Organization(name=org_name, slug=slug)
            self.org_service.repository.session.add(org)
            await self.org_service.repository.session.flush()

            # Make user org admin
            member = OrgMember(user_id=new_user.id, org_id=org.id, role=OrgRole.admin)
            self.org_service.repository.session.add(member)

            await self.user_repository.session.commit()

            # Refresh to get fully loaded objects if needed, or simply return
            await self.user_repository.session.refresh(new_user)
            await self.org_service.repository.session.refresh(org)

            return {
                "user": new_user,
                "organization": org
            }
        except Exception as e:
            await self.user_repository.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")

    async def login_user(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        if not user.is_active:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def refresh_tokens(self, refresh_token: str) -> dict:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        access_token = create_access_token(data={"sub": user_id})
        new_refresh_token = create_refresh_token(data={"sub": user_id})

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
