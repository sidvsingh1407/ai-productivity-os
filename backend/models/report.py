import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, func, Uuid, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("audits.id"), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    audit = relationship("Audit", back_populates="reports")

class ExportJobType(enum.Enum):
    pdf = "pdf"
    csv = "csv"
    json = "json"

class ExportJobStatus(enum.Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"

class ExportJob(Base):
    __tablename__ = "export_jobs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    job_type: Mapped[ExportJobType] = mapped_column(Enum(ExportJobType), nullable=False)
    status: Mapped[ExportJobStatus] = mapped_column(Enum(ExportJobStatus), nullable=False)
    result_path: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="export_jobs")
