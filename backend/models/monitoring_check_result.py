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

class MonitoringCheckResult(Base):
    __tablename__ = "monitoring_check_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    monitoring_plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monitoring_plans.id"), nullable=False, index=True)
    ai_system_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_systems.id"), nullable=False, index=True)

    findings: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    severity: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    monitoring_plan = relationship("MonitoringPlan")
    ai_system = relationship("AISystem")
