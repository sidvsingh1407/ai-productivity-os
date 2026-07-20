import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.prompt_engineer_usage import PromptEngineerUsage
from prompt_engineer_usage.schemas import PromptEngineerUsageCreate

class PromptEngineerUsageService:
    async def log_usage(self, db: AsyncSession, organization_id: uuid.UUID, data: PromptEngineerUsageCreate) -> PromptEngineerUsage:
        new_usage = PromptEngineerUsage(
            organization_id=organization_id,
            **data.model_dump()
        )
        db.add(new_usage)
        await db.commit()
        await db.refresh(new_usage)
        return new_usage

    async def list_usage(
        self,
        db: AsyncSession,
        organization_id: uuid.UUID,
        subscription_id: Optional[uuid.UUID] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[PromptEngineerUsage]:
        stmt = (
            select(PromptEngineerUsage)
            .where(PromptEngineerUsage.organization_id == organization_id)
        )

        if subscription_id:
            stmt = stmt.where(PromptEngineerUsage.subscription_id == subscription_id)

        stmt = (
            stmt
            .order_by(PromptEngineerUsage.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await db.execute(stmt)
        return list(result.scalars().all())
