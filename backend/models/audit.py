import uuid
import enum
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class AuditStatusEnum(str, enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class Audit(Base):
    __tablename__ = "audits"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    form_response: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    scores: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    total_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rating: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    compliance_risk_flag: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    compliance_risk_reasons: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    status: Mapped[AuditStatusEnum] = mapped_column(SQLAlchemyEnum(AuditStatusEnum))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="audits")
    user: Mapped["User"] = relationship("User", back_populates="audits")
    versions: Mapped[list["AuditVersion"]] = relationship("AuditVersion", back_populates="audit", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship("Report", back_populates="audit", cascade="all, delete-orphan")
    integration_results: Mapped[list["IntegrationResult"]] = relationship("IntegrationResult", back_populates="audit", cascade="all, delete-orphan")

class AuditVersion(Base):
    __tablename__ = "audit_versions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id", ondelete="CASCADE"))
    version_number: Mapped[int] = mapped_column(Integer)
    scores_snapshot: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    audit: Mapped["Audit"] = relationship("Audit", back_populates="versions")
