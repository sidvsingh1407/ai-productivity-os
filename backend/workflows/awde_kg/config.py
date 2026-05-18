from __future__ import annotations

from dataclasses import dataclass, field


RANKING_WEIGHTS = {
    "enterprise_process_fit": 0.30,
    "friction_clarity": 0.20,
    "automation_potential": 0.20,
    "hitl_compliance_relevance": 0.15,
    "dataset_metadata_quality": 0.10,
    "license_usability": 0.05,
}

DATASET_SCORE_FLOOR = 0.70
CONFIDENCE_FLOOR = 0.65
CATALOG_REFRESH_DAYS = 60

EDGE_TYPES = {
    "SUPPORTS_PROCESS",
    "HAS_SAMPLE",
    "EVIDENCES_FRICTION",
    "REQUIRES_CAPABILITY",
    "GENERATES_BLUEPRINT",
    "REQUIRES_HITL",
}

AUTOMATION_TIERS = {"full", "hitl", "augmented"}
BLUEPRINT_STATUSES = {"active", "deprecated", "under_review"}
IMPLEMENTATION_OUTCOMES = {"success", "partial", "failed"}
FAILURE_SIGNAL_TYPES = {
    "tool_unavailable",
    "wrong_process_match",
    "compliance_gap",
    "hitl_insufficient",
    "other",
}

ENTERPRISE_KEYWORDS = {
    "finance",
    "invoice",
    "tax",
    "erp",
    "reconciliation",
    "audit",
    "procurement",
    "vendor",
    "purchase",
    "contract",
    "legal",
    "compliance",
    "policy",
    "hr",
    "human resources",
    "employee",
    "payroll",
    "benefits",
    "customer support",
    "ticket",
    "crm",
    "sales",
    "lead",
    "it",
    "incident",
    "security",
    "operations",
    "supply chain",
    "healthcare",
    "claims",
    "insurance",
    "banking",
}

FRICTION_KEYWORDS = {
    "extract",
    "classification",
    "summarization",
    "document",
    "pdf",
    "email",
    "form",
    "manual",
    "review",
    "approval",
    "match",
    "cross-reference",
    "validate",
    "normalize",
    "routing",
}

AUTOMATION_KEYWORDS = {
    "workflow",
    "agent",
    "tool",
    "api",
    "json",
    "webhook",
    "database",
    "rpa",
    "ocr",
    "pipeline",
    "automation",
    "orchestration",
    "structured",
}

HITL_KEYWORDS = {
    "compliance",
    "regulated",
    "approval",
    "risk",
    "legal",
    "audit",
    "financial",
    "medical",
    "healthcare",
    "pii",
    "security",
    "discrepancy",
}

INSPECTABLE_EXTENSIONS = (
    ".json",
    ".jsonl",
    ".csv",
    ".parquet",
    ".arrow",
    ".txt",
)

LICENSE_TAG_PREFIX = "license:"
KNOWN_OPEN_LICENSES = {
    "mit",
    "apache-2.0",
    "bsd-3-clause",
    "bsd-2-clause",
    "cc-by-4.0",
    "cc-by-sa-4.0",
    "cc0-1.0",
    "odc-by",
    "openrail",
}


@dataclass(frozen=True)
class BuildConfig:
    target_min: int = 500
    target_max: int = 1000
    samples_per_repo_min: int = 10
    samples_per_repo_max: int = 20
    dataset_score_floor: float = DATASET_SCORE_FLOOR
    confidence_floor: float = CONFIDENCE_FLOOR
    ranking_weights: dict[str, float] = field(default_factory=lambda: dict(RANKING_WEIGHTS))
