import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from database import Base

# Use JSONB for Postgres, but gracefully fallback to JSON for SQLite in tests
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

class AdoptionRecord(Base):
    __tablename__ = "adoption_records"
    __table_args__ = (
        UniqueConstraint('ai_system_id', 'department', name='uix_ai_system_department'),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    ai_system_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_systems.id"), nullable=False, index=True)
    department: Mapped[str] = mapped_column(String, nullable=False)

    user_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    usage_frequency: Mapped[str] = mapped_column(String, nullable=False, default='not_specified')
    shadow_ai_detected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    champions: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    resistance_level: Mapped[str] = mapped_column(String, nullable=False, default='not_specified')
    training_status: Mapped[str] = mapped_column(String, nullable=False, default='not_specified')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization")
    # Using one-directional relationship as per memory rules
    ai_system = relationship("AISystem")
