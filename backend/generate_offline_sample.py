import json
import uuid
from datetime import datetime

# Adjust Python path to run locally
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from audits.scoring_engine import score_response
from audits.intelligence_engine import generate_intelligence

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

def generate_offline_sample():
    scores = score_response(SAMPLE_FORM_RESPONSE)
    intelligence = generate_intelligence(scores)

    report = {
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

    with open("offline_sample_payload.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    generate_offline_sample()
    print("Done")
