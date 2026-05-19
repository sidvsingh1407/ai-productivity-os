import uuid
import enum
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey, func, Uuid, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class WorkflowStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class Workflow(Base):
    __tablename__ = "workflows"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    input_config: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    status: Mapped[WorkflowStatus] = mapped_column(SQLAlchemyEnum(WorkflowStatus), default=WorkflowStatus.pending, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="workflows")
    user: Mapped["User"] = relationship("User", back_populates="workflows")
    blueprints: Mapped[list["Blueprint"]] = relationship("Blueprint", back_populates="workflow", cascade="all, delete-orphan")
    integration_results: Mapped[list["IntegrationResult"]] = relationship("IntegrationResult", back_populates="workflow", cascade="all, delete-orphan")

class Blueprint(Base):
    __tablename__ = "blueprints"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False)
    process_id: Mapped[str] = mapped_column(String, nullable=False)
    automation_tier: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    industry_variant: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    blueprint_data: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    merged: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="blueprints")

class IntegrationResult(Base):
    __tablename__ = "integration_results"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("audits.id", ondelete="CASCADE"), nullable=False)
    workflow_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False)
    recommendations: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Relationships
    audit: Mapped["Audit"] = relationship("Audit", back_populates="integration_results")
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="integration_results")