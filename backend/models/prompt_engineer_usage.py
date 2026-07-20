import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class PromptEngineerUsage(Base):
    __tablename__ = "prompt_engineer_usage"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    subscription_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("prompt_engineer_subscriptions.id"), nullable=False, index=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    usage_type: Mapped[str] = mapped_column(String, nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    request_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    model_used: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    subscription = relationship("PromptEngineerSubscription")
    organization = relationship("Organization")
