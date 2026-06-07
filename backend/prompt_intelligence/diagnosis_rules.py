ELEMENT_RULES = {
    "Context": ["context", "background", "situation", "scenario", "environment", "setting"],
    "Constraints": ["must", "should", "limit", "budget", "timeframe", "max", "min", "constraint", "only", "requirements", "limitations"],
    "Ownership": ["owner", "responsible", "role", "team", "assignee", "manager", "accountable"],
    "Outputs": ["table", "json", "report", "summary", "bullet", "format", "csv", "output", "markdown", "deliverable"],
    "Escalation Paths": ["escalation", "fallback", "exception", "review", "error", "fail", "issue", "blocker"]
}

ELEMENT_PENALTIES = {
    "Context": 20,
    "Constraints": 20,
    "Ownership": 20,
    "Outputs": 20,
    "Escalation Paths": 20
}

STRENGTH_THRESHOLDS = {
    "Strong": (90, 100),
    "Adequate": (70, 89),
    "Weak": (40, 69),
    "Broken": (0, 39)
}

EXECUTION_RISKS_MAPPING = {
    "Context": "Lack of Clear Purpose",
    "Constraints": "Inconsistent Responses",
    "Ownership": "Misaligned Recommendations",
    "Outputs": "Ambiguous Output",
    "Escalation Paths": "Failure During Edge Cases"
}
