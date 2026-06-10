import logging
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from users.repository import UserRepository
from organizations.service import OrganizationService
from auth.password_utils import hash_password, verify_password
from auth.jwt_utils import create_access_token, create_refresh_token, decode_token
from models.user import User
from models.organization import Organization, OrgMember, OrgRole
from models.user_token import UserToken
from tasks.email_tasks import send_email_task
from tasks.dispatch import safe_task_dispatch
from config import settings

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)
        self.org_service = OrganizationService(session)

    async def _generate_unique_org_slug(self, org_name: str) -> str:
        base_slug = self.org_service._generate_slug(org_name) or "organization"
        slug = base_slug
        suffix = 2

        while True:
            result = await self.session.execute(
                select(Organization.id).where(Organization.slug == slug)
            )
            if result.scalar_one_or_none() is None:
                return slug
            slug = f"{base_slug}-{suffix}"
            suffix += 1

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    async def _create_user_token(self, user_id, token_type: str, expiry_hours: int = 1) -> str:
        raw_token = secrets.token_urlsafe(32)
        token_hash = self._hash_token(raw_token)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=expiry_hours)

        user_token = UserToken(
            user_id=user_id,
            token_hash=token_hash,
            token_type=token_type,
            expires_at=expires_at
        )
        self.session.add(user_token)
        await self.session.flush()
        return raw_token

    async def register_user(self, email: str, password: str, full_name: str, org_name: str) -> dict:
        try:
            existing_user = await self.user_repository.get_by_email(email)
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

            # Create user
            hashed_pwd = hash_password(password)
            new_user = User(email=email, hashed_password=hashed_pwd, full_name=full_name)
            self.user_repository.session.add(new_user)
            await self.user_repository.session.flush()

            # Create organization
            slug = await self._generate_unique_org_slug(org_name)
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

            # Trigger Welcome and Verification Emails
            verify_token = await self._create_user_token(new_user.id, "EMAIL_VERIFICATION", expiry_hours=24)
            await self.session.commit()

            # Send background tasks
            safe_task_dispatch(
                send_email_task,
                new_user.email,
                "welcome",
                {"name": new_user.full_name, "frontend_url": settings.FRONTEND_URL}
            )

            safe_task_dispatch(
                send_email_task,
                new_user.email,
                "verify_email",
                {"verify_url": f"{settings.FRONTEND_URL}/verify-email?token={verify_token}"}
            )

            access_token = create_access_token(data={"sub": str(new_user.id)})
            refresh_token = create_refresh_token(data={"sub": str(new_user.id)})

            return {
                "user": new_user,
                "org": org,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        except HTTPException:
            raise
        except IntegrityError:
            await self.user_repository.session.rollback()
            logger.exception("Registration failed due to database integrity error")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or organization already exists",
            )
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            await self.user_repository.session.rollback()
            logger.exception(f"Registration failed due to unexpected backend error. Type: {type(e).__name__}, Message: {str(e)}, Traceback: {tb}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed",
            )

    async def login_user(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        if not user.is_active:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        # Get primary organization for the user
        orgs = await self.org_service.get_user_organizations(user.id)
        primary_org = orgs[0] if orgs else None

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "user": user,
            "org": primary_org,
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

    async def forgot_password(self, email: str):
        user = await self.user_repository.get_by_email(email)
        if user:
            reset_token = await self._create_user_token(user.id, "PASSWORD_RESET", expiry_hours=1)
            await self.session.commit()
            safe_task_dispatch(
                send_email_task,
                user.email,
                "password_reset",
                {"reset_url": f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"}
            )

    async def reset_password(self, token: str, new_password: str):
        token_hash = self._hash_token(token)
        result = await self.session.execute(
            select(UserToken).where(
                UserToken.token_hash == token_hash,
                UserToken.token_type == "PASSWORD_RESET",
                UserToken.used_at.is_(None)
            )
        )
        user_token = result.scalar_one_or_none()

        if not user_token or user_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

        user = await self.user_repository.get_by_id(user_token.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        user.hashed_password = hash_password(new_password)
        user_token.used_at = datetime.now(timezone.utc)
        await self.session.commit()

    async def verify_email(self, token: str):
        token_hash = self._hash_token(token)
        result = await self.session.execute(
            select(UserToken).where(
                UserToken.token_hash == token_hash,
                UserToken.token_type == "EMAIL_VERIFICATION",
                UserToken.used_at.is_(None)
            )
        )
        user_token = result.scalar_one_or_none()

        if not user_token or user_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

        user = await self.user_repository.get_by_id(user_token.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        user.email_verified = True
        user.email_verified_at = datetime.now(timezone.utc)
        user_token.used_at = datetime.now(timezone.utc)
        await self.session.commit()

    async def resend_verification(self, email: str):
        user = await self.user_repository.get_by_email(email)
        if user and not user.email_verified:
            verify_token = await self._create_user_token(user.id, "EMAIL_VERIFICATION", expiry_hours=24)
            await self.session.commit()
            safe_task_dispatch(
                send_email_task,
                user.email,
                "verify_email",
                {"verify_url": f"{settings.FRONTEND_URL}/verify-email?token={verify_token}"}
            )

    async def change_password(self, user: User, current_password: str, new_password: str):
        # need to fetch fresh user with hashed password since current_user from Depends(get_current_user) may not have it if omitted in schema
        user_with_pwd = await self.user_repository.get_by_id(user.id)

        if not verify_password(current_password, user_with_pwd.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid current password")

        user_with_pwd.hashed_password = hash_password(new_password)
        await self.session.commit()
