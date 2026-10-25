import sys
import os

if os.environ.get("ENVIRONMENT") == "production":
    print("ERROR: Cannot run data mutation/schema creation script in production.")
    sys.exit(1)
elif not os.environ.get("I_KNOW_WHAT_I_AM_DOING") == "true" and os.environ.get("ENVIRONMENT") != "testing":
    print("ERROR: Explicit opt-in required in non-production. Set I_KNOW_WHAT_I_AM_DOING=true.")
    sys.exit(1)

import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database import Base
import models
from models.audit import Audit
from models.system_finding import SystemFinding
from organizations.service import OrganizationService
from models.organization import Organization
from models.user import User
from models.workflow import Workflow, WorkflowStatus
from models.engineering_record import EngineeringRecord
from models.ai_system import AISystem
from models.adoption_record import AdoptionRecord
from adoption.scoring import calculate_adoption_score
from data_intelligence.scoring import calculate_data_score
from engineering.service import EngineeringRecordsService
from auth.password_service import PasswordService

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        org = Organization(name="Test", slug="test")
        db.add(org)
        await db.commit()
        await db.refresh(org)

        # --- LOW SCORE ---
        print("=== LOW SCORE ===")
        eng_low = EngineeringRecord(
            organization_id=org.id,
            has_mlops_pipeline=False,
            has_dedicated_ai_team=False,
            has_dedicated_prompt_engineer=False,
            has_dedicated_devops=False,
        )
        print("Engineering Low:", EngineeringRecordsService()._calculate_score(eng_low))

        sys_low = AISystem(
            organization_id=org.id,
            name="Low",
            data_types=["Other"]
        )
        print("Data Low:", calculate_data_score(sys_low))

        ad_low = AdoptionRecord(
            user_count=1,
            usage_frequency="rare",
            training_status="none"
        )
        print("Adoption Low:", calculate_adoption_score(ad_low))

        # --- PARTIAL SCORE ---
        print("=== PARTIAL SCORE ===")
        sys_part = AISystem(
            organization_id=org.id,
            name="Part",
            data_types=["PII"]
        )
        print("Data Partial:", calculate_data_score(sys_part))

        ad_part = AdoptionRecord(
            user_count=50,
            usage_frequency="weekly",
            training_status="in_progress"
        )
        print("Adoption Partial:", calculate_adoption_score(ad_part))

asyncio.run(main())
