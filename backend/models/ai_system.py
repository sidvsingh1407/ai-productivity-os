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

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # onupdate is enforced at the ORM level; this table has no direct SQL write path.
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization")
