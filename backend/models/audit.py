import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, func, Uuid, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class AuditStatus(enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class Audit(Base):
    __tablename__ = "audits"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    form_response: Mapped[dict] = mapped_column(JSONB, nullable=False)
    scores: Mapped[dict] = mapped_column(JSONB, nullable=False)
    total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[str] = mapped_column(String, nullable=False)
    compliance_risk_flag: Mapped[bool] = mapped_column(Boolean, nullable=False)
    compliance_risk_reasons: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[AuditStatus] = mapped_column(Enum(AuditStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="audits")
    organization = relationship("Organization", back_populates="audits")
    versions = relationship("AuditVersion", back_populates="audit")
    reports = relationship("Report", back_populates="audit")
    integration_results = relationship("IntegrationResult", back_populates="audit")

class AuditVersion(Base):
    __tablename__ = "audit_versions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("audits.id"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    scores_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Relationships
    audit = relationship("Audit", back_populates="versions")
