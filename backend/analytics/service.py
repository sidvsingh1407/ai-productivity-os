from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date, Float
from datetime import datetime, timezone, timedelta
import uuid

from models.audit import Audit

async def get_score_trend(db: AsyncSession, org_id: uuid.UUID | str, days: int = 30) -> list[dict]:
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Cast created_at to DATE to group by day
    date_col = cast(Audit.created_at, Date).label('date')
    avg_score_col = func.avg(Audit.total_score).label('avg_score')

    stmt = (
        select(date_col, avg_score_col)
        .where(Audit.org_id == org_id)
        .where(Audit.created_at >= start_date)
        .group_by(date_col)
        .order_by(date_col)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [{"date": row.date, "avg_score": float(row.avg_score)} for row in rows]

async def get_dimension_averages(db: AsyncSession, org_id: uuid.UUID | str) -> dict:
    # Use postgres JSONB operators to extract scores.
    # Example JSON: {"awareness": 80, "adoption": 70, ...}

    def extract_avg(field: str):
        # cast text to float for aggregation
        return func.avg(cast(Audit.scores[field].astext, Float)).label(field)

    stmt = select(
        extract_avg("awareness"),
        extract_avg("adoption"),
        extract_avg("integration"),
        extract_avg("governance"),
        extract_avg("roi")
    ).where(Audit.org_id == org_id)

    result = await db.execute(stmt)
    row = result.first()

    if row and any(v is not None for v in row):
        return {
            "awareness": float(row.awareness or 0),
            "adoption": float(row.adoption or 0),
            "integration": float(row.integration or 0),
            "governance": float(row.governance or 0),
            "roi": float(row.roi or 0),
        }
    else:
        return {
            "awareness": 0.0,
            "adoption": 0.0,
            "integration": 0.0,
            "governance": 0.0,
            "roi": 0.0,
        }

async def get_audit_volume(db: AsyncSession, org_id: uuid.UUID | str, days: int = 30) -> dict:
    total_audits = await db.scalar(select(func.count(Audit.id)).where(Audit.org_id == org_id))

    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    audits_this_period = await db.scalar(
        select(func.count(Audit.id))
        .where(Audit.org_id == org_id)
        .where(Audit.created_at >= start_date)
    )

    return {
        "total_audits": total_audits or 0,
        "audits_this_period": audits_this_period or 0
    }

async def get_compliance_rate(db: AsyncSession, org_id: uuid.UUID | str) -> dict:
    total_count = await db.scalar(select(func.count(Audit.id)).where(Audit.org_id == org_id))
    flagged_count = await db.scalar(
        select(func.count(Audit.id))
        .where(Audit.org_id == org_id)
        .where(Audit.compliance_risk_flag == True)
    )

    total = total_count or 0
    flagged = flagged_count or 0
    flag_rate_pct = (flagged / total * 100) if total > 0 else 0.0

    return {
        "flagged_count": flagged,
        "total_count": total,
        "flag_rate_pct": round(flag_rate_pct, 2)
    }
