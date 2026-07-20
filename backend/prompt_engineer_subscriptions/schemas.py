import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal

class PromptEngineerSubscriptionBase(BaseModel):
    plan_tier: str = Field(default='unset', min_length=1, description="Subscription plan tier")
    status: Literal['active', 'inactive', 'past_due', 'cancelled'] = Field(default='inactive', description="Subscription status")
    external_subscription_id: Optional[str] = Field(default=None, description="External billing provider subscription ID")
    seat_count: int = Field(default=1, ge=1, description="Number of seats included in the subscription")
    billing_cycle: Optional[str] = Field(default=None, description="Billing cycle (e.g. monthly, annual)")

class PromptEngineerSubscriptionCreate(PromptEngineerSubscriptionBase):
    pass

class PromptEngineerSubscriptionUpdate(BaseModel):
    plan_tier: Optional[str] = Field(default=None, min_length=1)
    status: Optional[Literal['active', 'inactive', 'past_due', 'cancelled']] = None
    external_subscription_id: Optional[str] = None
    seat_count: Optional[int] = Field(default=None, ge=1)
    billing_cycle: Optional[str] = None

class PromptEngineerSubscriptionResponse(PromptEngineerSubscriptionBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PromptEngineerSubscriptionListResponse(PromptEngineerSubscriptionResponse):
    pass
