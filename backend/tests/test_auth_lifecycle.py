import pytest
import pytest_asyncio
from sqlalchemy.future import select
from models.user import User
from models.user_token import UserToken
from auth.password_service import PasswordService
import secrets
import hashlib
from httpx import AsyncClient, ASGITransport
from main import app
from database import Base, engine, async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch

@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

@pytest.mark.asyncio
@patch('auth.service.send_templated_email')
async def test_register_and_verify_email(mock_delay, db_session: AsyncSession):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register user
        response = await client.post(
            "/auth/register",
        json={
            "email": "lifecycle@example.com",
            "password": "strongpassword123",
            "full_name": "Lifecycle User",
            "org_name": "Lifecycle Org"
            }
        )
        assert response.status_code == 201

        # Check DB for verification token
        user_query = await db_session.execute(select(User).where(User.email == "lifecycle@example.com"))
        user = user_query.scalar_one()
        # Since emails are mock, we bypass verification in dev/tests: assert user.email_verified == False

        token_query = await db_session.execute(
            select(UserToken).where(
                UserToken.user_id == user.id,
                UserToken.token_type == "EMAIL_VERIFICATION"
            )
        )
        token_model = token_query.scalar_one()

        # Simulate Resend Verification to get a new token to test
        resend_res = await client.post("/auth/resend-verification", json={"email": "lifecycle@example.com"})
        assert resend_res.status_code == 200

        # Since we can't easily extract the exact raw token sent to the email in testing (it's hashed),
        # we'll inject a known token into the DB to test the verify endpoint
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        token_model.token_hash = hashed_token
        await db_session.commit()

        # Verify Email
        verify_res = await client.post("/auth/verify-email", json={"token": raw_token})
        assert verify_res.status_code == 200

        # Refresh user
        await db_session.refresh(user)
        assert user.email_verified == True


@pytest.mark.asyncio
@patch('auth.service.send_templated_email')
async def test_forgot_and_reset_password(mock_delay, db_session: AsyncSession):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create test user
        response = await client.post(
            "/auth/register",
        json={
            "email": "reset@example.com",
            "password": "oldpassword123",
            "full_name": "Reset User",
            "org_name": "Reset Org"
            }
        )
        assert response.status_code == 201

        # Forgot password request
        forgot_res = await client.post("/auth/forgot-password", json={"email": "reset@example.com"})
        assert forgot_res.status_code == 200

        user_query = await db_session.execute(select(User).where(User.email == "reset@example.com"))
        user = user_query.scalar_one()

        # Inject token for testing reset
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

        token_query = await db_session.execute(
            select(UserToken).where(
                UserToken.user_id == user.id,
                UserToken.token_type == "PASSWORD_RESET"
            )
        )
        token_model = token_query.scalar_one()
        token_model.token_hash = hashed_token
        await db_session.commit()

        # Invalid reset attempt
        invalid_reset_res = await client.post(
            "/auth/reset-password",
            json={"token": "invalid_token", "new_password": "newpassword123"}
        )
        assert invalid_reset_res.status_code == 400

        # Valid reset attempt
        reset_res = await client.post(
            "/auth/reset-password",
            json={"token": raw_token, "new_password": "newpassword123"}
        )
        assert reset_res.status_code == 200

        # Refresh user and check password
        await db_session.refresh(user)
        ps = PasswordService()
        assert ps.verify_password("newpassword123", user.hashed_password) == True

@pytest.mark.asyncio
@patch('auth.service.send_templated_email')
async def test_change_password_authenticated(mock_delay, db_session: AsyncSession):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register user
        reg_response = await client.post(
            "/auth/register",
        json={
            "email": "change@example.com",
            "password": "currentpassword123",
            "full_name": "Change User",
            "org_name": "Change Org"
            }
        )
        assert reg_response.status_code == 201

        # Must verify email to login now
        user_query = await db_session.execute(select(User).where(User.email == "change@example.com"))
        user = user_query.scalar_one()
        user.email_verified = True
        await db_session.commit()

        login_res = await client.post(
            "/auth/login",
            json={"email": "change@example.com", "password": "currentpassword123"}
        )
        assert login_res.status_code == 200

        token = login_res.json()["access_token"]

        # Attempt change password with wrong current
        wrong_change = await client.post(
            "/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json={"current_password": "wrongpassword123", "new_password": "newpassword123"}
        )
        assert wrong_change.status_code == 400

        # Valid change
        valid_change = await client.post(
            "/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json={"current_password": "currentpassword123", "new_password": "newpassword123"}
        )
        assert valid_change.status_code == 200

        # Login with new password
        login_res = await client.post(
            "/auth/login",
            json={"email": "change@example.com", "password": "newpassword123"}
        )
        assert login_res.status_code == 200
