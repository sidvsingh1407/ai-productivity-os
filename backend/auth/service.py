import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from users.repository import UserRepository
from organizations.service import OrganizationService
from auth.password_service import PasswordService
from auth.token_service import TokenService
from auth.token_repository import TokenRepository
from models.user import User
from models.organization import Organization, OrgMember, OrgRole
from utils.email import send_templated_email
from fastapi import BackgroundTasks
from config import settings

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, session: AsyncSession, background_tasks: BackgroundTasks = None):
        self.session = session
        self.background_tasks = background_tasks
        self.user_repository = UserRepository(session)
        self.org_service = OrganizationService(session)
        self.password_service = PasswordService()
        self.token_repository = TokenRepository(session)
        self.token_service = TokenService(repository=self.token_repository)

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

    async def register_user(self, email: str, password: str, full_name: str, org_name: str) -> dict:
        try:
            existing_user = await self.user_repository.get_by_email(email)
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

            if not self.password_service.validate_password(password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is too weak")

            hashed_pwd = self.password_service.hash_password(password)
            new_user = User(email=email, hashed_password=hashed_pwd, full_name=full_name)
            self.user_repository.session.add(new_user)
            await self.user_repository.session.flush()

            slug = await self._generate_unique_org_slug(org_name)
            org = Organization(name=org_name, slug=slug)
            self.org_service.repository.session.add(org)
            await self.org_service.repository.session.flush()

            member = OrgMember(user_id=new_user.id, org_id=org.id, role=OrgRole.admin)
            self.org_service.repository.session.add(member)

            await self.user_repository.session.commit()

            await self.user_repository.session.refresh(new_user)
            await self.org_service.repository.session.refresh(org)

            verify_token = await self.token_service.create_verification_token(new_user.id)
            await self.session.commit()

            if self.background_tasks:
                self.background_tasks.add_task(
                    send_templated_email,
                    new_user.email,
                    "welcome",
                    {"name": new_user.full_name, "frontend_url": settings.FRONTEND_URL}
                )
                self.background_tasks.add_task(
                    send_templated_email,
                    new_user.email,
                    "verify_email",
                    {"verify_url": f"{settings.FRONTEND_URL}/verify-email?token={verify_token}"}
                )

            return {
                "message": "Registration successful. Please verify your email.",
                "user": new_user
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
        try:
            user = await self.user_repository.get_by_email(email)
            if not user or not self.password_service.verify_password(password, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.exception(f"Login failed due to unexpected backend error. Type: {type(e).__name__}, Message: {str(e)}, Traceback: {tb}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed",
            )

        try:
            if not user.is_active:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

            if not user.email_verified:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please verify your email before logging in.")

            orgs = await self.org_service.get_user_organizations(user.id)
            primary_org = orgs[0] if orgs else None

            access_token = self.token_service.create_access_token(data={"sub": str(user.id)})
            refresh_token = await self.token_service.create_refresh_token(user.id)

            await self.session.commit()

            return {
                "user": user,
                "org": primary_org,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.exception(f"Login failed due to unexpected backend error (second part). Type: {type(e).__name__}, Message: {str(e)}, Traceback: {tb}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed",
            )

    async def refresh_tokens(self, refresh_token: str) -> dict:
        payload = await self.token_service.verify_refresh_token(refresh_token)
        user_id_str = payload.get("sub")
        old_jti = payload.get("jti")

        user_id = UUID(user_id_str)

        # Refresh token rotation: revoke old token, issue new one
        await self.token_service.revoke_single_refresh_token(old_jti)

        access_token = self.token_service.create_access_token(data={"sub": str(user_id)})
        new_refresh_token = await self.token_service.create_refresh_token(user_id)

        await self.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    async def logout(self, current_user: User, refresh_token: str = None):
        """Invalidates the provided refresh token, or all tokens if not provided."""
        if refresh_token:
            try:
                # We don't want to throw an error on logout if token is already invalid,
                # just decode statelessly to grab JTI and revoke if we can.
                payload = self.token_service.verify_token(refresh_token)
                jti = payload.get("jti")
                if jti:
                    await self.token_service.revoke_single_refresh_token(jti)
            except Exception:
                # Fallback to revoking all if something went wrong with decoding
                await self.token_service.revoke_refresh_tokens(current_user.id)
        else:
            await self.token_service.revoke_refresh_tokens(current_user.id)

        await self.session.commit()

    async def forgot_password(self, email: str):
        user = await self.user_repository.get_by_email(email)
        if user:
            reset_token = await self.token_service.create_password_reset_token(user.id)
            await self.session.commit()
            if self.background_tasks:
                self.background_tasks.add_task(
                    send_templated_email,
                    user.email,
                    "password_reset",
                    {"reset_url": f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"}
                )

    async def reset_password(self, token: str, new_password: str):
        if not self.password_service.validate_password(new_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is too weak")

        user_token = await self.token_repository.get_token(token, "PASSWORD_RESET")

        if not user_token or user_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

        user = await self.user_repository.get_by_id(user_token.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        user.hashed_password = self.password_service.hash_password(new_password)
        await self.token_repository.mark_used(user_token)

        # Revoke all existing refresh tokens
        await self.token_service.revoke_refresh_tokens(user.id)

        await self.session.commit()

    async def verify_email(self, token: str):
        user_token = await self.token_repository.get_token(token, "EMAIL_VERIFICATION")

        if not user_token or user_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

        user = await self.user_repository.get_by_id(user_token.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        user.email_verified = True
        user.email_verified_at = datetime.now(timezone.utc)
        await self.token_repository.mark_used(user_token)
        await self.session.commit()

    async def resend_verification(self, email: str):
        user = await self.user_repository.get_by_email(email)
        if user and not user.email_verified:
            verify_token = await self.token_service.create_verification_token(user.id)
            await self.session.commit()
            if self.background_tasks:
                self.background_tasks.add_task(
                    send_templated_email,
                    user.email,
                    "verify_email",
                    {"verify_url": f"{settings.FRONTEND_URL}/verify-email?token={verify_token}"}
                )

    async def change_password(self, user: User, current_password: str, new_password: str):
        user_with_pwd = await self.user_repository.get_by_id(user.id)

        if not self.password_service.verify_password(current_password, user_with_pwd.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid current password")

        if not self.password_service.validate_password(new_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is too weak")

        user_with_pwd.hashed_password = self.password_service.hash_password(new_password)

        # Revoke all existing refresh tokens
        await self.token_service.revoke_refresh_tokens(user.id)

        await self.session.commit()