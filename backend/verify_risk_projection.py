import json
from audits.intelligence_engine import generate_intelligence

def verify_risk_projection():
    print("--- Case A: High/Critical Risk (Low Governance, Low Integration) ---")
    case_a_scores = {
        'total_score': 42,
        'dimensions': {
            'governance': 5,     # 25/100
            'integration': 7,    # 35/100
            'adoption': 12,      # 60/100
            'awareness': 10,     # 50/100
            'roi': 8             # 40/100
        },
        'compliance_risk_flag': False,
        'compliance_risk_reasons': [],
        'missing_data_flags': [],
        'contradictions': []
    }

    intel_a = generate_intelligence(case_a_scores)
    risk_a = intel_a.get("risk_projection", {})
    print(json.dumps(risk_a, indent=2))
    assert risk_a.get("risk_level") in ["High", "Critical"], f"Expected High or Critical, got {risk_a.get('risk_level')}"

    print("\n--- Case B: Low Risk (High Maturity Across Dimensions) ---")
    case_b_scores = {
        'total_score': 85,
        'dimensions': {
            'governance': 17,    # 85/100
            'integration': 17,   # 85/100
            'adoption': 18,      # 90/100
            'awareness': 16,     # 80/100
            'roi': 17            # 85/100
        },
        'compliance_risk_flag': False,
        'compliance_risk_reasons': [],
        'missing_data_flags': [],
        'contradictions': []
    }

    intel_b = generate_intelligence(case_b_scores)
    risk_b = intel_b.get("risk_projection", {})
    print(json.dumps(risk_b, indent=2))
    assert risk_b.get("risk_level") == "Low", f"Expected Low, got {risk_b.get('risk_level')}"

    print("\nVerification successful!")

if __name__ == "__main__":
    verify_risk_projection()
