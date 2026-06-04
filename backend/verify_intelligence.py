import json
from audits.intelligence_engine import generate_intelligence
from audits.intelligence_rules import determine_severity

def main():
    print("=" * 60)
    print("TarkaX Sprint 3A - Intelligence Engine Verification")
    print("=" * 60)

    # 1. Verification of Rule Examples
    print("\n--- Rule Examples ---")
    score_examples = [25, 45, 60, 85]
    for score in score_examples:
        sev = determine_severity(score)
        print(f"Score {score} -> Severity: {sev}")

    print("\nGovernance score 25 Example:")
    gov_test_scores = {
        'dimensions': {'governance': 5}, # 5 * 5 = 25
        'compliance_risk_flag': False,
        'contradictions': [],
        'missing_data_flags': []
    }
    gov_intel = generate_intelligence(gov_test_scores)

    print("-> Finding:")
    print(json.dumps(gov_intel["findings"][0], indent=2))
    print("-> Recommendation:")
    print(json.dumps(gov_intel["recommendations"][0], indent=2))


    # 2. Sample Input / Full Payload
    print("\n\n--- Sample Input ---")
    sample_scores = {
        'dimensions': {
            'awareness': 10,  # 50 - Major
            'adoption': 12,   # 60 - Moderate
            'integration': 7, # 35 - Critical
            'governance': 8,  # 40 - Major
            'roi': 15         # 75 - Advisory
        },
        'compliance_risk_flag': True,
        'compliance_risk_reasons': ['q4_1', 'q4_2'],
        'contradictions': ["Strong ROI claimed without sufficient supporting explanation."],
        'missing_data_flags': ['roi']
    }
    print(json.dumps(sample_scores, indent=2))

    # 3. Sample Output
    print("\n--- Sample Generated Output ---")
    intelligence_output = generate_intelligence(sample_scores)
    print(json.dumps(intelligence_output, indent=2))

    print("\n" + "=" * 60)
    print("Verification Complete.")

if __name__ == "__main__":
    main()
