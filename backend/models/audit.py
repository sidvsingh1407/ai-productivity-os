import uuid
import enum
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func, Uuid, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class AuditStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class Audit(Base):
    __tablename__ = "audits"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    form_response: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    scores: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    total_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rating: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    compliance_risk_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    compliance_risk_reasons: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    status: Mapped[AuditStatus] = mapped_column(SQLAlchemyEnum(AuditStatus), default=AuditStatus.pending, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="audits")
    user: Mapped["User"] = relationship("User", back_populates="audits")
    versions: Mapped[list["AuditVersion"]] = relationship("AuditVersion", back_populates="audit", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship("Report", back_populates="audit", cascade="all, delete-orphan")
    integration_results: Mapped[list["IntegrationResult"]] = relationship("IntegrationResult", back_populates="audit", cascade="all, delete-orphan")

class AuditVersion(Base):
    __tablename__ = "audit_versions"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("audits.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    scores_snapshot: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    audit: Mapped["Audit"] = relationship("Audit", back_populates="versions")
