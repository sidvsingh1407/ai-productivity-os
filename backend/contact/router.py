from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.contact import ContactLead

router = APIRouter(tags=["Contact"])

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None
    interest: str | None = None
    message: str | None = None
    source_page: str | None = None
    consent_given: bool = False

class ContactResponse(BaseModel):
    success: bool
    message: str

@router.post("/contact", response_model=ContactResponse)
async def submit_contact(req: ContactRequest, db: AsyncSession = Depends(get_db)):
    try:
        new_lead = ContactLead(
            name=req.name,
            email=req.email,
            company=req.company,
            interest=req.interest,
            message=req.message,
            source_page=req.source_page,
            consent_given=req.consent_given
        )
        db.add(new_lead)
        await db.commit()
        return ContactResponse(success=True, message="Your request has been received.")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save contact request")
