import uuid
import enum
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Enum, func, Boolean, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class ApiTier(str, enum.Enum):
    free = "free"
    pro = "pro"
    enterprise = "enterprise"


class ApiKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    key_hash: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    tier: Mapped[ApiTier] = mapped_column(Enum(ApiTier), default=ApiTier.free, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization = relationship("Organization")
    usage_logs = relationship("ApiUsageLog", back_populates="api_key", cascade="all, delete-orphan")


class ApiUsageLog(Base):
    __tablename__ = "api_usage_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    api_key_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("api_keys.id"), nullable=False)
    endpoint: Mapped[str] = mapped_column(String, nullable=False)
    request_method: Mapped[str] = mapped_column(String, nullable=False)
    response_status: Mapped[int] = mapped_column(Integer, nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    api_key = relationship("ApiKey", back_populates="usage_logs")
