import re

with open('backend/tests/test_6_6a_scores.py', 'r') as f:
    content = f.read()

# Update test_data_score to match the new additive scoring model
new_content = re.sub(
    r'def test_data_score\(\):.*?def test_roi_score_structural_output\(\):',
    """def test_data_score():
    # 1. High Score Scenario (all 5 fields meaningfully populated)
    high_system = {
        "data_sensitivity": "medium",
        "data_freshness": "real_time",
        "data_owner": "user@example.com",
        "data_accessibility": ["internal_only"],
        "data_types": ["PII"]
    }
    assert calculate_data_score(high_system) == 100.0

    # 2. Medium Score Scenario (3 of 5 fields populated)
    medium_system = {
        "data_owner": "user@example.com",
        "data_types": ["PII"],
        "data_sources": ["DB1"] # data_sources + data_types only gives one 20pt bump
    }
    assert calculate_data_score(medium_system) == 40.0

    # 3. Low Score Scenario (1 of 5 fields populated)
    low_system = {
        "data_types": ["Financial"]
    }
    assert calculate_data_score(low_system) == 20.0

def test_roi_score_structural_output():""",
    content,
    flags=re.DOTALL
)

with open('backend/tests/test_6_6a_scores.py', 'w') as f:
    f.write(new_content)
