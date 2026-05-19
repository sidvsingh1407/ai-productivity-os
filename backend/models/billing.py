import uuid
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, Integer, DateTime, ForeignKey, func, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class BillingPlan(Base):
    __tablename__ = "billing_plans"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price_monthly: Mapped[int] = mapped_column(Integer, nullable=False) # in cents
    max_audits_per_month: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_users: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    features: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    # Relationships
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="plan")
class Subscription(Base):
    __tablename__ = "subscriptions"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), unique=True, nullable=False)
    plan_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("billing_plans.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String, default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="subscription")
    plan: Mapped["BillingPlan"] = relationship("BillingPlan", back_populates="subscriptions")
