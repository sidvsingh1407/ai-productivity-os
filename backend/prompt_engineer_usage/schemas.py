import uuid
from pydantic import BaseModel, Field
from typing import Optional

class PromptEngineerUsageCreate(BaseModel):
    subscription_id: uuid.UUID
    usage_type: str
    token_count: int = Field(default=0)
    request_count: int = Field(default=1)
    model_used: Optional[str] = None

    model_config = {
        "protected_namespaces": ()
    }
