import asyncio
import sys
import uuid

# Import ALL models so registry resolves correctly
from backend.models.user import User
from backend.models.organization import Organization, OrgMember
from backend.models.ai_system import AISystem
from backend.models.audit import Audit
from backend.models.system_finding import SystemFinding
# We just need to import backend.database
from backend.database import Base

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///backend/local_test.db"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def seed():
    async with async_session() as db:
        # Create user
        uid = uuid.uuid4().hex
        email = "playwright@test.com"
        user = User(
            id=uid,
            full_name="Test User",
            email=email,
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # "password"
            is_active=True,
            email_verified=True,
            is_superadmin=False
        )
        db.add(user)

        # Create org
        org_id = uuid.uuid4().hex
        org = Organization(
            id=org_id,
            name="Test Org",
            slug=f"org-{uuid.uuid4().hex[:8]}"
        )
        db.add(org)
        await db.commit()

        # Add member
        member = OrgMember(
            user_id=uid,
            org_id=org_id,
            role="owner"
        )
        db.add(member)

        # Create system 1
        sys1 = AISystem(
            id=uuid.uuid4().hex,
            organization_id=org_id,
            name="Test System",
            ai_type="generative",
            criticality="high",
            lifecycle_status="deployed",
            department="engineering",
            owner="Playwright",
            adoption_record={"status": "in_progress", "details": "Some adoption"},
            cost_currency="USD"
        )
        db.add(sys1)

        await db.commit()
        print(f"Seeded successfully. Playwright user: {email} / password")

asyncio.run(seed())
