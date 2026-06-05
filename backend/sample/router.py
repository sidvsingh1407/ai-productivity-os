from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import uuid
from datetime import datetime

from audits.scoring_engine import score_response
from audits.intelligence_engine import generate_intelligence
from benchmarking.adapter import get_api_benchmark_payload
from audits.repository import get_all_completed_audits

router = APIRouter(tags=["Sample Report"])

SAMPLE_FORM_RESPONSE = {
    "q1_1": "c",
    "q1_2": "b",
    "q1_3": "c",
    "q2_1": "d",
    "q2_2": "c",
    "q2_3": "b",
    "q3_1": "c",
    "q3_2": "d",
    "q3_3": "b",
    "q4_1": "d",
    "q4_2": "d",
    "q4_3": "b",
    "q5_1": "c",
    "q5_2": "b",
    "q5_3": "c"
}

@router.get("/sample-report")
async def get_sample_report(db: AsyncSession = Depends(get_db)):
    """Generates a dynamic sample report via the AI Audit scoring engine"""

    # Run the deterministic scoring engine on a pre-defined sample payload
    scores = score_response(SAMPLE_FORM_RESPONSE)

    # Generate full intelligence payload
    intelligence = generate_intelligence(scores)

    # Generate benchmark intelligence
    completed_audits = await get_all_completed_audits(db)
    org_total_score = scores.get('total_score', 0)
    org_dimension_scores = scores.get('dimensions', {})
    benchmark_payload = get_api_benchmark_payload(
        organization_total_score=org_total_score,
        organization_dimension_scores=org_dimension_scores,
        assessments=completed_audits
    )
    intelligence["benchmark"] = benchmark_payload

    return {
        "id": str(uuid.uuid4()),
        "org_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "form_response": SAMPLE_FORM_RESPONSE,
        "evidence_response": {},
        "scores": scores.get('dimensions', {}),
        "total_score": scores.get('total_score', 0),
        "rating": scores.get('rating', 'AI Emerging'),
        "compliance_risk_flag": scores.get('compliance_risk_flag', False),
        "compliance_risk_reasons": scores.get('compliance_risk_reasons', []),
        "contradictions": scores.get('contradictions', []),
        "missing_data_flags": scores.get('missing_data_flags', []),
        "evidence_quality_score": scores.get('evidence_quality_score', 0),
        "confidence_index": scores.get('confidence_index', 0),
        "intelligence": intelligence,
        "status": "complete",
        "created_at": datetime.utcnow().isoformat()
    }
