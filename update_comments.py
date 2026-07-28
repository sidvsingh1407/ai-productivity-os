import re

with open('backend/tests/test_6_6d_readiness_score.py', 'r') as f:
    content = f.read()

# Update High Score
content = re.sub(
    r'# System scores: Adoption=100, Data=100 \(due to many fields\), ROI=100 \(\(50000 - 15000\)/15000 -> capped at 100\)\n *# Average System score = ~100\n *\n *# Total Readiness Score = \(95.0 \* 0.5\) \+ \(100 \* 0.5\) = 97.5',
    """# System scores (excluding ROI which evaluates to None):
    # - Adoption = 100.0 (user_count=100, daily freq, training completed)
    # - Data = 100.0 (all fields populated)
    # Average System score = (100.0 + 100.0) / 2 = 100.0

    # Operational Score = (90 * 0.5) + (75 * 0.5) = 82.5
    # Total Readiness Score = (100.0 * 0.5) + (82.5 * 0.5) = 91.25""",
    content
)

# Update Low Score
content = re.sub(
    r'# Expected: System scores: Adoption=0, Data=15 \(just type\), ROI=0 \(loss\)\n *# Average System score = 5.0\n *# Total Readiness = \(5.0 \* 0.5\) \+ \(5.0 \* 0.5\) = 5.0',
    """# System scores (excluding ROI which evaluates to None):
    # - Adoption = 12.5 (user_count=1 -> 25 base, rare freq * 0.5)
    # - Data = 85.0 (minimal fields populated)
    # Average System score = (12.5 + 85.0) / 2 = 48.75

    # Operational Score = (10 * 0.5) + (0 * 0.5) = 5.0
    # Total Readiness Score = (48.75 * 0.5) + (5.0 * 0.5) = 26.875""",
    content
)

# Update Partial Score
content = re.sub(
    r'# System scores: Adoption=50, Data=15, ROI=None\n *# System avg: 32.5\n *# Since operational is None, readiness should be the system average = 32.5',
    """# System scores (excluding ROI which evaluates to None):
    # - Adoption = 60.0 (user_count=50 -> 50 base, weekly freq * 1.0, training in_progress + 10)
    # - Data = 85.0 (minimal fields populated)
    # Average System score = (60.0 + 85.0) / 2 = 72.5

    # Operational Score = None (Missing workflows and engineering)
    # Total Readiness Score = System average (fallback redistribution) = 72.5""",
    content
)

with open('backend/tests/test_6_6d_readiness_score.py', 'w') as f:
    f.write(content)
