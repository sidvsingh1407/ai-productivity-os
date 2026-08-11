import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class WorkflowRecommendation(Base):
    __tablename__ = "workflow_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    opportunity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_recommendation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("agent_recommendations.id", ondelete="SET NULL"), nullable=True, index=True)

    recommendation_type: Mapped[str] = mapped_column(String, nullable=False)
    rationale: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    organization = relationship("Organization")
    opportunity = relationship("Opportunity")
    agent_recommendation = relationship("AgentRecommendation")

    __table_args__ = (
        UniqueConstraint('opportunity_id', 'recommendation_type', name='uix_opportunity_recommendation_type'),
    )
