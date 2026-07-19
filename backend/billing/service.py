import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.billing import Subscription, BillingPlan
from billing.schemas import SubscriptionStatus

logger = logging.getLogger(__name__)

async def get_org_subscription_status(db: AsyncSession, org_id: uuid.UUID) -> SubscriptionStatus:
    stmt = (
        select(BillingPlan)
        .join(Subscription, Subscription.plan_id == BillingPlan.id)
        .where(Subscription.org_id == org_id)
        .where(Subscription.status == "active")
    )
    result = await db.execute(stmt)
    plan = result.scalar_one_or_none()

    if plan:
        return SubscriptionStatus(
            tier=plan.name,
            max_audits_per_month=plan.max_audits_per_month,
            max_users=plan.max_users,
            max_ai_systems=None, # will be added in 1.4b
            features=plan.features
        )
    else:
        logger.warning(f"Organization {org_id} has no assigned subscription plan. Defaulting to 'starter' tier.")
        return SubscriptionStatus(
            tier="starter",
            max_audits_per_month=1,
            max_users=1,
            max_ai_systems=None,
            features={}
        )
