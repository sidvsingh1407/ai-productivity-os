import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class SavedPromptBase(BaseModel):
    title: Optional[str] = None
    original_prompt: str
    improved_prompt: Optional[str] = None

class SavedPromptCreate(SavedPromptBase):
    pass

class SavedPromptResponse(SavedPromptBase):
    id: uuid.UUID
    project_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectListResponse(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    saved_prompts_count: int
    model_config = ConfigDict(from_attributes=True)

class ProjectDetailResponse(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    saved_prompts: List[SavedPromptResponse] = []
    model_config = ConfigDict(from_attributes=True)
