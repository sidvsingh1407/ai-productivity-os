import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class DependencyNode(Base):
    __tablename__ = "dependency_nodes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    node_type: Mapped[str] = mapped_column(String, nullable=False)

    ai_system_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=True, index=True)
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("workflows.id", ondelete="CASCADE"), nullable=True, index=True)
    audit_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("audits.id", ondelete="CASCADE"), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "(ai_system_id IS NOT NULL AND workflow_id IS NULL AND audit_id IS NULL AND node_type = 'ai_system') OR "
            "(workflow_id IS NOT NULL AND ai_system_id IS NULL AND audit_id IS NULL AND node_type = 'workflow') OR "
            "(audit_id IS NOT NULL AND ai_system_id IS NULL AND workflow_id IS NULL AND node_type = 'audit')",
            name="check_node_type_fk_alignment"
        ),
    )


class DependencyEdge(Base):
    __tablename__ = "dependency_edges"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    source_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dependency_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    target_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dependency_nodes.id", ondelete="CASCADE"), nullable=False, index=True)

    edge_type: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
