import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class Blueprint(Base):
    __tablename__ = "blueprints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"))
    data = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class IntegrationResult(Base):
    __tablename__ = "integration_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id = Column(UUID(as_uuid=True), ForeignKey("audits.id"))
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"))
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))

    recommendations = Column(JSONB, nullable=True)
    audit_score_summary = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
