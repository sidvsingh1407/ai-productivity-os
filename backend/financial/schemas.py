from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class OrgCostData(BaseModel):
    total: float
    is_partial: bool
    systems_with_data: int
    total_systems: int

class FinancialIntelligenceResponse(BaseModel):
    org_cost: OrgCostData
    cost_by_criticality: Dict[str, OrgCostData]
