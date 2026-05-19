import uuid
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, func, Uuid, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class ExportJobType(str, enum.Enum):
    pdf = "pdf"
    csv = "csv"
    json = "json"

class ExportJobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class Report(Base):
    __tablename__ = "reports"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("audits.id", ondelete="CASCADE"), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # Relationships
    audit: Mapped["Audit"] = relationship("Audit", back_populates="reports")

class ExportJob(Base):
    __tablename__ = "export_jobs"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_type: Mapped[ExportJobType] = mapped_column(SQLAlchemyEnum(ExportJobType), nullable=False)
    status: Mapped[ExportJobStatus] = mapped_column(SQLAlchemyEnum(ExportJobStatus), default=ExportJobStatus.pending, nullable=False)
    result_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="export_jobs")