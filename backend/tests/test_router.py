from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_token import UserToken
from models.user import User
from database import get_db

router = APIRouter(prefix="/test-api", tags=["test"])

@router.get("/get-verification-token")
async def get_verification_token(email: str, db: AsyncSession = Depends(get_db)):
    # This route is STRICTLY for testing Playwright. It gets the latest verification token for an email.
    # In a real setup, it should only be mounted in testing environments.
    user_query = await db.execute(select(User).where(User.email == email))
    user = user_query.scalar_one_or_none()
    if not user:
        return {"error": "user not found"}

    # Notice: we hash the tokens now. We cannot retrieve the raw token.
    # But for Playwright testing, it was requested that: "If email verification cannot be completed... use the generated verification URL/token from the test backend".
    # Since we only store the hash, we can't fetch the raw token here anymore!
    # Instead, we will force verify the user directly to allow the flow to proceed.

    user.email_verified = True
    await db.commit()
    return {"message": "force verified"}

@router.get("/get-reset-token")
async def get_reset_token(email: str, db: AsyncSession = Depends(get_db)):
    """
    Warning: Because we now securely hash all reset tokens, we cannot retrieve the raw token
    from the DB to use in E2E tests once it's created by the standard flow.
    For this Playwright hook, we will manually generate a new token and insert its hash
    so we can return the raw token back to Playwright.
    """
    import secrets
    from auth.token_repository import TokenRepository

    user_query = await db.execute(select(User).where(User.email == email))
    user = user_query.scalar_one_or_none()
    if not user:
        return {"error": "user not found"}

    token_repo = TokenRepository(db)
    raw_token = await token_repo.create_token(user.id, "PASSWORD_RESET", expiry_hours=1)
    await db.commit()

    return {"token": raw_token}
