import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from models.risk_classification import RiskClassification
from models.ai_system_cost_snapshot import AISystemCostSnapshot

RISK_LEVEL_SCORES = {
    "unacceptable": 30,
    "high_risk": 25,
    "ambiguous": 15,
    "limited_risk": 10,
    "minimal_risk": 0
}

async def calculate_risk_trend(db: AsyncSession, ai_system_id: uuid.UUID) -> str:
    """
    Determines the risk trend by comparing the two most recent RiskClassifications for a system.
    Returns "Increasing", "Decreasing", "Stable", or "insufficient_data".
    """
    stmt = select(RiskClassification).where(
        RiskClassification.ai_system_id == ai_system_id
    ).order_by(
        desc(RiskClassification.created_at)
    ).limit(2)

    result = await db.execute(stmt)
    records = result.scalars().all()

    if len(records) < 2:
        return "insufficient_data"

    recent = records[0]
    previous = records[1]

    recent_score = RISK_LEVEL_SCORES.get(recent.risk_level, 0)
    previous_score = RISK_LEVEL_SCORES.get(previous.risk_level, 0)

    if recent_score > previous_score:
        return "Increasing"
    elif recent_score < previous_score:
        return "Decreasing"
    else:
        return "Stable"

async def calculate_financial_trend(db: AsyncSession, ai_system_id: uuid.UUID) -> dict:
    """
    Determines the financial trend by comparing the two most recent AISystemCostSnapshots.
    Returns direction, raw delta, percentage change, and partial data caveats.
    """
    stmt = select(AISystemCostSnapshot).where(
        AISystemCostSnapshot.ai_system_id == ai_system_id
    ).order_by(
        desc(AISystemCostSnapshot.created_at)
    ).limit(2)

    result = await db.execute(stmt)
    snapshots = result.scalars().all()

    if len(snapshots) < 2:
        return {"direction": "insufficient_data"}

    recent = snapshots[0]
    previous = snapshots[1]

    recent_cost = float(recent.total_cost or 0.0)
    previous_cost = float(previous.total_cost or 0.0)

    delta = recent_cost - previous_cost

    # Calculate percentage change
    if previous_cost == 0:
        if recent_cost > 0:
            percentage_change = float('inf') # Or some representation of 100% / infinite increase
            direction = "Increasing"
        elif recent_cost < 0:
            percentage_change = float('-inf')
            direction = "Decreasing"
        else:
            percentage_change = 0.0
            direction = "Stable"
    else:
        percentage_change = (delta / previous_cost) * 100

        if percentage_change > 5.0:
            direction = "Increasing"
        elif percentage_change < -5.0:
            direction = "Decreasing"
        else:
            direction = "Stable"

    response = {
        "direction": direction,
        "delta": delta,
        "percentage_change": percentage_change,
        "is_partial_comparison": recent.is_partial or previous.is_partial
    }

    if response["is_partial_comparison"]:
        response["caveat"] = "Note: Comparison involves partial cost data and may not represent the full financial trend."

    return response
