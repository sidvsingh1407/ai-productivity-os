ELEMENT_RULES = {
    "Objective": ["create", "build", "generate", "analyze", "evaluate"],
    "Audience": ["manager", "executive", "consultant", "stakeholder", "customer", "team", "audience"],
    "Output Format": ["table", "json", "bullet", "report", "markdown", "format", "csv"],
    "Constraints": ["must", "should", "limit", "budget", "timeframe", "max", "min", "constraint", "only"],
    "Success Criteria": ["success", "kpi", "metric", "outcome", "goal", "target"],
    "Exception Handling": ["if", "when", "exception", "fallback", "escalation", "error", "fail"],
    "Decision Criteria": ["criteria", "basis", "factor", "reason", "condition"]
}

ELEMENT_PENALTIES = {
    "Objective": 25,
    "Output Format": 20,
    "Audience": 15,
    "Success Criteria": 15,
    "Exception Handling": 15,
    "Constraints": 10,
    "Decision Criteria": 10  # Added to ensure complete coverage, will cap deduction anyway
}

STRENGTH_THRESHOLDS = {
    "Strong": (90, 100),
    "Adequate": (70, 89),
    "Weak": (40, 69),
    "Broken": (0, 39)
}

EXECUTION_RISKS_MAPPING = {
    "Output Format": "Ambiguous Output",
    "Audience": "Misaligned Recommendations",
    "Success Criteria": "Unmeasurable Outcome",
    "Exception Handling": "Failure During Edge Cases",
    "Constraints": "Inconsistent Responses",
    "Decision Criteria": "Subjective Recommendations",
    "Objective": "Lack of Clear Purpose"
}
