import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from database import Base
import enum

class AuditStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class Audit(Base):
    __tablename__ = "audits"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    form_response: Mapped[dict] = mapped_column(JSONB, nullable=False)
    evidence_response: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    total_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    evidence_quality_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    contradictions: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    rating: Mapped[str | None] = mapped_column(String, nullable=True)
    compliance_risk_flag: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    compliance_risk_reasons: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[AuditStatus] = mapped_column(Enum(AuditStatus), default=AuditStatus.pending, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    versions = relationship("AuditVersion", back_populates="audit")

class AuditVersion(Base):
    __tablename__ = "audit_versions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    scores_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    audit = relationship("Audit", back_populates="versions")
