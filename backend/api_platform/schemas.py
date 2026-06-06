from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from models.audit import IndustryType

class AuditApiRequest(BaseModel):
    form_response: Dict[str, Any]
    evidence_response: Optional[Dict[str, Any]] = None
    industry_type: Optional[IndustryType] = None

class RiskApiScores(BaseModel):
    dimensions: Dict[str, int]
    missing_data_flags: Optional[List[str]] = []
    contradictions: Optional[List[str]] = []
    evidence_quality_score: Optional[int] = 100

class RiskApiRequest(BaseModel):
    scores: RiskApiScores
    findings: Optional[List[Dict[str, Any]]] = []
