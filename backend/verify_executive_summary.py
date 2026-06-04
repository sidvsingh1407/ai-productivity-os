import json
from audits.intelligence_engine import generate_intelligence

def verify_case(name: str, scores: dict):
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    print(f"Input Scores:\n{json.dumps(scores, indent=2)}")
    output = generate_intelligence(scores)
    print(f"\nExecutive Summary:\n{json.dumps(output['executive_summary'], indent=2)}")

def main():
    print("Verification of Executive Summary Engine")

    # 1. High Maturity Organization
    high_maturity = {
        'dimensions': {
            'awareness': 18,
            'adoption': 16,
            'integration': 17,
            'governance': 18,
            'roi': 15
        },
        'confidence_index': 90,
        'compliance_risk_flag': False,
        'compliance_risk_reasons': [],
        'contradictions': [],
        'missing_data_flags': []
    }
    verify_case("High Maturity Organization", high_maturity)

    # 2. Medium Maturity Organization
    medium_maturity = {
        'dimensions': {
            'awareness': 14,
            'adoption': 12,
            'integration': 10,
            'governance': 13,
            'roi': 11
        },
        'confidence_index': 65,  # Reduced confidence
        'compliance_risk_flag': False,
        'compliance_risk_reasons': [],
        'contradictions': ["Standardized workflow claimed but manual workarounds referenced."],
        'missing_data_flags': []
    }
    verify_case("Medium Maturity Organization (Low Confidence, Contradictions)", medium_maturity)

    # 3. Low Maturity Organization
    low_maturity = {
        'dimensions': {
            'awareness': 8,
            'adoption': 6,
            'integration': 4,
            'governance': 5,  # 5 * 5 = 25 (Critical Governance Risk)
            'roi': 5
        },
        'confidence_index': 80,
        'compliance_risk_flag': True,
        'compliance_risk_reasons': ["q4_1", "q4_2"],
        'contradictions': [],
        'missing_data_flags': []
    }
    verify_case("Low Maturity Organization (Compliance Risk, Critical Governance)", low_maturity)

    # 4. Low Maturity Organization (Integration Bottleneck)
    low_maturity_integration = {
        'dimensions': {
            'awareness': 10,
            'adoption': 8,
            'integration': 2, # Lowest dimension
            'governance': 10,
            'roi': 8
        },
        'confidence_index': 80,
        'compliance_risk_flag': False,
        'compliance_risk_reasons': [],
        'contradictions': [],
        'missing_data_flags': []
    }
    verify_case("Low Maturity Organization (Integration Critical Risk)", low_maturity_integration)


if __name__ == "__main__":
    main()