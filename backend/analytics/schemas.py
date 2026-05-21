from pydantic import BaseModel
from datetime import date

class ScoreTrendItem(BaseModel):
    date: date
    avg_score: float

class DimensionAverages(BaseModel):
    awareness: float
    adoption: float
    integration: float
    governance: float
    roi: float

class AuditVolume(BaseModel):
    total_audits: int
    audits_this_period: int

class ComplianceRate(BaseModel):
    flagged_count: int
    total_count: int
    flag_rate_pct: float
