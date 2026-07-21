import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class RiskClassification(Base):
    __tablename__ = "risk_classifications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id"), nullable=False, index=True)
    ai_system_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_systems.id"), nullable=False, index=True)

    risk_level: Mapped[str] = mapped_column(String, nullable=False)
    matched_category: Mapped[str | None] = mapped_column(String, nullable=True)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    citation_reference: Mapped[str] = mapped_column(Text, nullable=False)
    requires_human_review: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    audit = relationship("Audit")
    ai_system = relationship("AISystem")
