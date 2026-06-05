import json
import uuid
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from audits.scoring_engine import score_response
from audits.intelligence_engine import generate_findings

# A perfectly scoring sample
HIGH_MATURITY_RESPONSE = {
    "q1_1": "d",
    "q1_2": "d",
    "q1_3": "d",
    "q2_1": "d",
    "q2_2": "d",
    "q2_3": "d",
    "q3_1": "d",
    "q3_2": "d",
    "q3_3": "d",
    "q4_1": "d",
    "q4_2": "d",
    "q4_3": "d",
    "q5_1": "d",
    "q5_2": "d",
    "q5_3": "d"
}

def test():
    scores = score_response(HIGH_MATURITY_RESPONSE)
    findings = generate_findings(scores)
    print("Findings length:", len(findings))
    print(json.dumps(findings, indent=2))

if __name__ == "__main__":
    test()
