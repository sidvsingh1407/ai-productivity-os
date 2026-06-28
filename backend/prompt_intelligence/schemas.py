from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any

class PromptRequest(BaseModel):
    prompt: str

class OperationalContext(BaseModel):
    detected_context: str
    purpose: str
    operational_environment: str

class DiagnosisResponse(BaseModel):
    strength: str
    missing_elements: List[str]
    execution_risks: List[str]

class ScoresResponse(BaseModel):
    original_score: int
    improved_score: int

class ValidationResponse(BaseModel):
    passed: bool
    validation_errors: List[str]

class RationaleResponse(BaseModel):
    context_reasoning: str
    changes_made: List[str]
    failure_modes_addressed: List[str]
    expected_improvements: str

class PromptResponse(BaseModel):
    operational_context: OperationalContext
    diagnosis: DiagnosisResponse
    improved_prompt: str
    improvement_rationale: RationaleResponse
    intelligence_scores: ScoresResponse
    validation: ValidationResponse

# New schemas for Prompt History
class PromptHistoryResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    original_prompt: str
    improved_prompt: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ValidationFailureResponse(BaseModel):
    validation: ValidationResponse
