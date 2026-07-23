import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean, UniqueConstraint, func, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from database import Base

# Use JSONB for Postgres, but gracefully fallback to JSON for SQLite in tests
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

class EngineeringRecord(Base):
    __tablename__ = "engineering_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, unique=True, index=True)

    has_dedicated_ai_team: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    team_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    roles: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    consultants_used: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)

    has_mlops_pipeline: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    monitoring_tooling: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    has_dedicated_prompt_engineer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    prompt_engineer_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    has_dedicated_devops: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    devops_support_type: Mapped[str] = mapped_column(String, nullable=False, default='not_specified')

    ai_engineering_budget: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    planned_investment_roadmap: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization")
