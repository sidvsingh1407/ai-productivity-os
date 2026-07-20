import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from models.prompt_engineer_subscription import PromptEngineerSubscription
from prompt_engineer_subscriptions.schemas import PromptEngineerSubscriptionCreate, PromptEngineerSubscriptionUpdate

class PromptEngineerSubscriptionsService:
    async def create_subscription(self, db: AsyncSession, organization_id: uuid.UUID, data: PromptEngineerSubscriptionCreate) -> PromptEngineerSubscription:
        new_subscription = PromptEngineerSubscription(
            organization_id=organization_id,
            **data.model_dump()
        )
        db.add(new_subscription)
        await db.commit()
        await db.refresh(new_subscription)
        return new_subscription

    async def list_subscriptions(self, db: AsyncSession, organization_id: uuid.UUID, limit: int = 50, offset: int = 0) -> List[PromptEngineerSubscription]:
        stmt = (
            select(PromptEngineerSubscription)
            .where(PromptEngineerSubscription.organization_id == organization_id)
            .order_by(PromptEngineerSubscription.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_subscription(self, db: AsyncSession, organization_id: uuid.UUID, subscription_id: uuid.UUID) -> PromptEngineerSubscription:
        stmt = select(PromptEngineerSubscription).where(
            PromptEngineerSubscription.id == subscription_id,
            PromptEngineerSubscription.organization_id == organization_id
        )
        result = await db.execute(stmt)
        subscription = result.scalar_one_or_none()

        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")

        return subscription

    async def update_subscription(self, db: AsyncSession, organization_id: uuid.UUID, subscription_id: uuid.UUID, data: PromptEngineerSubscriptionUpdate) -> PromptEngineerSubscription:
        subscription = await self.get_subscription(db, organization_id, subscription_id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(subscription, key, value)

        await db.commit()
        await db.refresh(subscription)
        return subscription

    async def delete_subscription(self, db: AsyncSession, organization_id: uuid.UUID, subscription_id: uuid.UUID):
        subscription = await self.get_subscription(db, organization_id, subscription_id)

        await db.delete(subscription)
        await db.commit()
        return {"status": "success"}
