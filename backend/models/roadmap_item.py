import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )

    source_type: Mapped[str] = mapped_column(String, nullable=False)

    opportunity_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=True, index=True
    )
    agent_recommendation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("agent_recommendations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    workflow_recommendation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("workflow_recommendations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    category: Mapped[str] = mapped_column(String, nullable=False)
    time_horizon: Mapped[str | None] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    department: Mapped[str | None] = mapped_column(String, nullable=True)
    owner: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    organization = relationship("Organization")
    opportunity = relationship("Opportunity")
    agent_recommendation = relationship("AgentRecommendation")
    workflow_recommendation = relationship("WorkflowRecommendation")

    __table_args__ = (
        CheckConstraint(
            "(opportunity_id IS NOT NULL AND agent_recommendation_id IS NULL AND workflow_recommendation_id IS NULL AND source_type = 'opportunity') OR "
            "(agent_recommendation_id IS NOT NULL AND opportunity_id IS NULL AND workflow_recommendation_id IS NULL AND source_type = 'agent_recommendation') OR "
            "(workflow_recommendation_id IS NOT NULL AND opportunity_id IS NULL AND agent_recommendation_id IS NULL AND source_type = 'workflow_recommendation')",
            name="check_roadmap_item_source_type_fk_alignment",
        ),
    )
