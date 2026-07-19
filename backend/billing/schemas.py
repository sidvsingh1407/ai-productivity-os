from pydantic import BaseModel
from typing import Optional, Dict, Any

class SubscriptionStatus(BaseModel):
    tier: str
    max_audits_per_month: Optional[int] = None
    max_users: Optional[int] = None
    max_ai_systems: Optional[int] = None
    features: Dict[str, Any]
