import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, func, Integer, Float, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from database import Base

# Use JSONB for Postgres, but gracefully fallback to JSON for SQLite in tests
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

class AISystem(Base):
    __tablename__ = "ai_systems"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_types: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    decision_making_role: Mapped[str] = mapped_column(String, nullable=False, default='not_specified')
    status: Mapped[str] = mapped_column(String, nullable=False, default='active')

    version: Mapped[str | None] = mapped_column(String, nullable=True)
    lifecycle_status: Mapped[str | None] = mapped_column(String, nullable=True)
    owner: Mapped[str | None] = mapped_column(String, nullable=True)
    department: Mapped[str | None] = mapped_column(String, nullable=True)
    business_capability: Mapped[str | None] = mapped_column(String, nullable=True)
    internal_external_users: Mapped[str | None] = mapped_column(String, nullable=True)
    criticality: Mapped[str | None] = mapped_column(String, nullable=True)
    implementation_stage: Mapped[str | None] = mapped_column(String, nullable=True)
    ai_type: Mapped[str | None] = mapped_column(String, nullable=True)

    vendor: Mapped[str | None] = mapped_column(String, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String, nullable=True)
    model_version: Mapped[str | None] = mapped_column(String, nullable=True)
    api_provider: Mapped[str | None] = mapped_column(String, nullable=True)
    framework: Mapped[str | None] = mapped_column(String, nullable=True)
    hosting: Mapped[str | None] = mapped_column(String, nullable=True)
    integrations: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    authentication_method: Mapped[str | None] = mapped_column(String, nullable=True)
    vector_db: Mapped[str | None] = mapped_column(String, nullable=True)
    knowledge_sources: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    workflow_engine: Mapped[str | None] = mapped_column(String, nullable=True)
    agent_framework: Mapped[str | None] = mapped_column(String, nullable=True)

    deployment_type: Mapped[str | None] = mapped_column(String, nullable=True)
    data_flow: Mapped[str | None] = mapped_column(Text, nullable=True)
    apis: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True, default=list)
    databases: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True, default=list)
    event_systems: Mapped[str | None] = mapped_column(Text, nullable=True)
    caching: Mapped[str | None] = mapped_column(Text, nullable=True)
    monitoring: Mapped[str | None] = mapped_column(Text, nullable=True)
    logging: Mapped[str | None] = mapped_column(Text, nullable=True)
    deployment_details: Mapped[str | None] = mapped_column(Text, nullable=True)

    data_sensitivity: Mapped[str | None] = mapped_column(String, nullable=True)
    data_sources: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True, default=list)
    data_destinations: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True, default=list)
    usage_frequency: Mapped[str | None] = mapped_column(String, nullable=True)
    users_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    uptime: Mapped[float | None] = mapped_column(Float, nullable=True)
    approvals_required: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)

    risk_classification: Mapped[str | None] = mapped_column(String, nullable=True)
    oversight_status: Mapped[str | None] = mapped_column(String, nullable=True)
    documentation_status: Mapped[str | None] = mapped_column(String, nullable=True)
    applicable_policies: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    rbac_enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    encryption_status: Mapped[str | None] = mapped_column(String, nullable=True)
    incident_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    applicable_regulations: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    obligations: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    evidence_status: Mapped[str | None] = mapped_column(String, nullable=True)
    cost: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    roi_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    licensing_type: Mapped[str | None] = mapped_column(String, nullable=True)
    planned_changes: Mapped[str | None] = mapped_column(Text, nullable=True)
    roadmap_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # onupdate is enforced at the ORM level; this table has no direct SQL write path.
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization")
