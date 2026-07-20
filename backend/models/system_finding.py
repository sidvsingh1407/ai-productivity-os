import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from database import Base

# Use JSONB for Postgres, but gracefully fallback to JSON for SQLite in tests
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

class SystemFinding(Base):
    __tablename__ = "system_findings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id"), nullable=False, index=True)
    ai_system_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_systems.id"), nullable=False, index=True)

    findings: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    recommendations: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    executive_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    dimension_scores: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    audit = relationship("Audit")
    ai_system = relationship("AISystem")
