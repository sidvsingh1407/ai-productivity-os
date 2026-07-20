import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class PromptEngineerSubscription(Base):
    __tablename__ = "prompt_engineer_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    plan_tier: Mapped[str] = mapped_column(String, nullable=False, default='unset')
    status: Mapped[str] = mapped_column(String, nullable=False, default='inactive')
    external_subscription_id: Mapped[str | None] = mapped_column(String, nullable=True)
    seat_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    billing_cycle: Mapped[str | None] = mapped_column(String, nullable=True, default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization")
