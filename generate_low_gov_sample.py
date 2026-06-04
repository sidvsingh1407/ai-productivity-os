import json
import uuid
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from audits.scoring_engine import score_response
from audits.intelligence_engine import generate_intelligence

# A low governance score sample
LOW_GOV_RESPONSE = {
    "q1_1": "c",
    "q1_2": "c",
    "q1_3": "c",
    "q2_1": "c",
    "q2_2": "c",
    "q2_3": "c",
    "q3_1": "c",
    "q3_2": "c",
    "q3_3": "c",
    "q4_1": "a", # Low governance
    "q4_2": "a", # Low governance
    "q4_3": "a", # Low governance
    "q5_1": "c",
    "q5_2": "c",
    "q5_3": "c"
}

def generate_low_gov():
    scores = score_response(LOW_GOV_RESPONSE)
    intelligence = generate_intelligence(scores)
    print("Low Gov COI generated:", len(intelligence.get("cost_of_inaction", [])))
    print(json.dumps(intelligence.get("cost_of_inaction", []), indent=2))

if __name__ == "__main__":
    generate_low_gov()
