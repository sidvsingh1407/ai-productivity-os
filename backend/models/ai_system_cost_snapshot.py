import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class AISystemCostSnapshot(Base):
    __tablename__ = "ai_system_cost_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    ai_system_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id", ondelete="CASCADE"), nullable=False, index=True)

    licensing_cost: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    cloud_cost: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    inference_cost: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    maintenance_cost: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    total_cost: Mapped[float | None] = mapped_column(Numeric, nullable=True)

    is_partial: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
