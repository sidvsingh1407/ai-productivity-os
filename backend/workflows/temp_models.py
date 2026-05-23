# TEMP MODEL - replace with backend/models/workflow.py after Phase 1 merge
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from database import Base
import uuid

class Workflow(Base):
    __tablename__ = "workflows"
    __table_args__ = {'extend_existing': True}
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(String, nullable=False, default="running")
    input_config = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Blueprint(Base):
    __tablename__ = "blueprints"
    __table_args__ = {'extend_existing': True}
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id"), nullable=False)
    process_id = Column(String, nullable=False)
    automation_tier = Column(String, nullable=False)
    industry_variant = Column(String, nullable=True)
    confidence = Column(Float, nullable=False)
    merged = Column(Boolean, default=False)
    blueprint_data = Column(JSONB, nullable=False)
