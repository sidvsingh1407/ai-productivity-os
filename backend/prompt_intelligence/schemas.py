from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any

class PromptRequest(BaseModel):
    prompt: str

class ContextResponse(BaseModel):
    category: str
    confidence: float

class DiagnosisResponse(BaseModel):
    strength: str
    missing: List[str]
    execution_risks: List[str]

class ScoresResponse(BaseModel):
    original_score: int
    improved_score: int

class ValidationResponse(BaseModel):
    passed: bool
    errors: List[str]

class RationaleResponse(BaseModel):
    changes_made: List[str]
    failure_modes_addressed: List[str]

class PromptResponse(BaseModel):
    context: ContextResponse
    diagnosis: DiagnosisResponse
    scores: ScoresResponse
    validation: ValidationResponse
    improved_prompt: str = ""
    rationale: RationaleResponse

class ValidationFailureResponse(BaseModel):
    validation: ValidationResponse
