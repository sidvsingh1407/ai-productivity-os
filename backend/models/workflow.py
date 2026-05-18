import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, Uuid, ForeignKey, Enum, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class WorkflowStatus(enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    input_config: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[WorkflowStatus] = mapped_column(Enum(WorkflowStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="workflows")
    organization = relationship("Organization", back_populates="workflows")
    blueprints = relationship("Blueprint", back_populates="workflow")
    integration_results = relationship("IntegrationResult", back_populates="workflow")

class Blueprint(Base):
    __tablename__ = "blueprints"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("workflows.id"), nullable=False)
    process_id: Mapped[str] = mapped_column(String, nullable=False)
    automation_tier: Mapped[str] = mapped_column(String, nullable=False)
    industry_variant: Mapped[str] = mapped_column(String, nullable=False)
    blueprint_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    merged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Relationships
    workflow = relationship("Workflow", back_populates="blueprints")

class IntegrationResult(Base):
    __tablename__ = "integration_results"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("audits.id"), nullable=False)
    workflow_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("workflows.id"), nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("organizations.id"), nullable=False)
    audit_score_summary: Mapped[dict] = mapped_column(JSONB, nullable=False)
    recommendations: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Relationships
    audit = relationship("Audit", back_populates="integration_results")
    workflow = relationship("Workflow", back_populates="integration_results")
    organization = relationship("Organization", back_populates="integration_results")
