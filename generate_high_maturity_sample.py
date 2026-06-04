import json
import uuid
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from audits.scoring_engine import score_response
from audits.intelligence_engine import generate_intelligence

# A perfectly scoring sample
HIGH_MATURITY_RESPONSE = {
    "q1_1": "a",
    "q1_2": "a",
    "q1_3": "a",
    "q2_1": "a",
    "q2_2": "a",
    "q2_3": "a",
    "q3_1": "a",
    "q3_2": "a",
    "q3_3": "a",
    "q4_1": "a",
    "q4_2": "a",
    "q4_3": "a",
    "q5_1": "a",
    "q5_2": "a",
    "q5_3": "a"
}

EVIDENCE_RESPONSE = {
    "q4_1": {"evidence_url": "https://example.com/policy"},
    "q2_1": {"evidence_url": "https://example.com/adoption"},
    "q3_1": {"evidence_url": "https://example.com/integration"},
    "q3_2": {"evidence_context": "Automated pipeline"},
    "q5_1": {"evidence_context": "Strong ROI with detailed explanation of over 30 chars for the rule to pass"}
}

def generate_high_maturity():
    scores = score_response(HIGH_MATURITY_RESPONSE, EVIDENCE_RESPONSE)
    intelligence = generate_intelligence(scores)
    print("High Maturity COI generated:", len(intelligence.get("cost_of_inaction", [])))
    print(json.dumps(intelligence.get("cost_of_inaction", []), indent=2))

if __name__ == "__main__":
    generate_high_maturity()
