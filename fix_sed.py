import re

with open('backend/tests/test_6_6d_readiness_score.py', 'r') as f:
    content = f.read()

# Update Low Score
content = re.sub(
    r'# -- MATH BREAKDOWN --\s*# Operational Score:\s*# Workflow \(10\.0\) and Engineering \(0\.0\) -> Average = \(10 \* 0\.5\) \+ \(0 \* 0\.5\) = 5\.0\s*#\s*# System Scores \(skipping ROI, which is unconditionally None due to text schema\):\s*# - Adoption = 12\.5 \(user_count=1 -> 25 base, rare freq \* 0\.5, training none \+ 0 = 12\.5\)\s*# - Data = 85\.0 \(Base 100\.0\. No data_owner -> -15 penalty\. data_freshness and data_sensitivity are None so no penalties for them\. 100 - 15 = 85\.0\)\s*# Average System score = \(12\.5 \+ 85\.0\) / 2 = 48\.75\s*#\s*# Total Readiness Score = \(48\.75 \(System\) \* 0\.5\) \+ \(5\.0 \(Operational\) \* 0\.5\) = 26\.875\s*score_data = await service\.get_readiness_score_data\(organization\.id\)\s*assert score_data\["readiness_score"\] == 26\.875',
    """# -- MATH BREAKDOWN --
    # Operational Score:
    # Workflow (10.0) and Engineering (0.0) -> Average = (10 * 0.5) + (0 * 0.5) = 5.0
    #
    # System Scores (skipping ROI, which is unconditionally None due to text schema):
    # - Adoption = 12.5 (user_count=1 -> 25 base, rare freq * 0.5, training none + 0 = 12.5)
    # - Data = 20.0 (Additive model: +20 for data_types array populated, 0 for missing owner/freshness/sensitivity/access)
    # Average System score = (12.5 + 20.0) / 2 = 16.25
    #
    # Total Readiness Score = (16.25 (System) * 0.5) + (5.0 (Operational) * 0.5) = 10.625

    score_data = await service.get_readiness_score_data(organization.id)

    assert score_data["readiness_score"] == 10.625""",
    content
)

with open('backend/tests/test_6_6d_readiness_score.py', 'w') as f:
    f.write(content)
