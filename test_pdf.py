import asyncio
import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "secret"
from audits.scoring_engine import score_response
from audits.intelligence_engine import generate_intelligence
from audits.schemas import AuditIntelligenceResponse
import json

def test():
    # just create a sample payload
    form_response = {
        "q2_1": "a", "q2_2": "a", "q2_3": "a",
        "q3_1": "a", "q3_2": "a", "q3_3": "a",
        "q4_1": "a", "q4_2": "a", "q4_3": "a",
        "q5_1": "a", "q5_2": "a", "q5_3": "a"
    }
    scores = score_response(form_response, None)
    intelligence = generate_intelligence(scores)

    # Try validating it
    AuditIntelligenceResponse(**intelligence)
    print("All good!")

test()
