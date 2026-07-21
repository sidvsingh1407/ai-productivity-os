import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from database import Base

# Use JSONB for Postgres, but gracefully fallback to JSON for SQLite in tests
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

class MonitoringPlan(Base):
    __tablename__ = "monitoring_plans"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    ai_system_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_systems.id"), nullable=False, index=True)
    risk_classification_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("risk_classifications.id"), nullable=True)

    status: Mapped[str] = mapped_column(String, nullable=False, default='draft')
    monitoring_scope: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    review_cadence: Mapped[str | None] = mapped_column(String, nullable=True)

    last_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization")
    ai_system = relationship("AISystem")
    risk_classification = relationship("RiskClassification")
