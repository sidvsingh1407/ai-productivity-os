from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, EmailStr
from typing import Optional
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from database import get_db
from models.waitlist_signup import WaitlistSignup
from config import settings
from utils.email import send_templated_email

router = APIRouter()

class WaitlistCreate(BaseModel):
    email: EmailStr
    product_preference: Optional[str] = None
    source: str

def hash_ip(ip: str) -> str:
    return hashlib.sha256(f"{ip}{settings.WAITLIST_IP_SALT}".encode()).hexdigest()

@router.post("")
async def create_waitlist_signup(
    signup: WaitlistCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    ip = request.client.host if request.client else "unknown"
    hashed_ip = hash_ip(ip)

    # Check rate limit (max 3 per IP hash per hour)
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    stmt = select(WaitlistSignup).where(
        WaitlistSignup.ip_hash == hashed_ip,
        WaitlistSignup.created_at >= one_hour_ago
    )
    recent_signups = (await db.execute(stmt)).scalars().all()
    if len(recent_signups) >= 3:
        raise HTTPException(status_code=429, detail="Too many requests")

    email = signup.email.lower().strip()

    # Check if already exists
    stmt = select(WaitlistSignup).where(WaitlistSignup.email == email)
    existing = (await db.execute(stmt)).scalar_one_or_none()

    confirmation_token = secrets.token_urlsafe(32)

    if existing:
        if existing.confirmed_at:
            return {"message": "Success"}

        # Regenerate token and resend
        existing.confirmation_token = confirmation_token
        await db.commit()
    else:
        new_signup = WaitlistSignup(
            email=email,
            product_preference=signup.product_preference,
            source=signup.source,
            ip_hash=hashed_ip,
            confirmation_token=confirmation_token
        )
        db.add(new_signup)
        await db.commit()

    # Send email in background
    confirm_url = f"{settings.FRONTEND_URL}/api/waitlist/confirm?token={confirmation_token}"
    unsubscribe_url = f"{settings.FRONTEND_URL}/api/waitlist/unsubscribe?token={confirmation_token}"
    background_tasks.add_task(
        send_templated_email,
        email,
        "waitlist_confirm",
        {"confirm_url": confirm_url, "unsubscribe_url": unsubscribe_url}
    )

    return {"message": "Success"}

from fastapi.responses import RedirectResponse

@router.get("/confirm")
async def confirm_waitlist(token: str, db: AsyncSession = Depends(get_db)):
    stmt = select(WaitlistSignup).where(WaitlistSignup.confirmation_token == token)
    signup = (await db.execute(stmt)).scalar_one_or_none()

    if not signup:
        return RedirectResponse(f"{settings.FRONTEND_URL}/expired")

    if signup.created_at < datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=7):
        return RedirectResponse(f"{settings.FRONTEND_URL}/expired")

    signup.confirmed_at = datetime.now(timezone.utc)
    signup.confirmation_token = None
    await db.commit()

    return RedirectResponse(f"{settings.FRONTEND_URL}/confirmed")
