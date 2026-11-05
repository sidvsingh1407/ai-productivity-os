from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import sqlalchemy as sa
from sqlalchemy.sql import func

class WaitlistSignup(Base):
    __tablename__ = "waitlist_signups"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    email = Column(String, nullable=False, unique=True)
    product_preference = Column(String, nullable=True)
    source = Column(String, nullable=False)
    ip_hash = Column(String, nullable=False)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    confirmation_token = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
