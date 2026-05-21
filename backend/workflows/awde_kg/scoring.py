from __future__ import annotations

from typing import Any

from .config import (
    AUTOMATION_KEYWORDS,
    ENTERPRISE_KEYWORDS,
    FRICTION_KEYWORDS,
    HITL_KEYWORDS,
    INSPECTABLE_EXTENSIONS,
    KNOWN_OPEN_LICENSES,
    LICENSE_TAG_PREFIX,
    BuildConfig,
)
from .util import clamp, text_blob


def score_record(record: dict[str, Any], config: BuildConfig) -> dict[str, Any]:
    tags = list(record.get("tags") or [])
    blob = text_blob(
        record.get("id"),
        record.get("description"),
        record.get("cardData"),
        record.get("task_categories"),
        record.get("paperswithcode_id"),
        tags,
    )
    sample_inspectability = is_sample_inspectable(record)
    license_status, license_score = score_license(tags, record)
    components = {
        "enterprise_process_fit": keyword_score(blob, ENTERPRISE_KEYWORDS),
        "friction_clarity": keyword_score(blob, FRICTION_KEYWORDS),
        "automation_potential": keyword_score(blob, AUTOMATION_KEYWORDS),
        "hitl_compliance_relevance": keyword_score(blob, HITL_KEYWORDS),
        "dataset_metadata_quality": metadata_quality(record),
        "license_usability": license_score,
    }
    weighted_score = 0.0
    for key, weight in config.ranking_weights.items():
        weighted_score += components[key] * weight
    weighted_score = round(clamp(weighted_score), 4)
    return {
        "sample_inspectability": sample_inspectability,
        "score_components": components,
        "enterprise_relevance_score": weighted_score,
        "license_status": license_status,
        "selected_for_graph": False,
        "score_explanation": explain_score(components, sample_inspectability, license_status),
    }


def select_records(records: list[dict[str, Any]], config: BuildConfig) -> list[dict[str, Any]]:
    scored = []
    for record in records:
        enriched = dict(record)
        enriched.update(score_record(record, config))
        if not enriched["sample_inspectability"]:
            enriched["rejection_reason"] = "sample_inspectability_false"
        elif enriched["enterprise_relevance_score"] < config.dataset_score_floor:
            enriched["rejection_reason"] = "below_score_floor"
        elif enriched["license_status"] == "unknown":
            enriched["rejection_reason"] = "unknown_license"
        else:
            scored.append(enriched)
    scored.sort(
        key=lambda item: (
            item["enterprise_relevance_score"],
            item.get("downloads") or 0,
            item.get("likes") or 0,
            item.get("id") or "",
        ),
        reverse=True,
    )
    selected = scored[: config.target_max]
    for item in selected:
        item["selected_for_graph"] = True
        item["status"] = item.get("status") or "active"
    return selected


def is_sample_inspectable(record: dict[str, Any]) -> bool:
    if record.get("viewer") is True or record.get("preview") is True:
        return True
    tags = [str(tag).lower() for tag in record.get("tags") or []]
    if "viewer" in tags or "preview" in tags:
        return True
    siblings = record.get("siblings") or []
    for sibling in siblings:
        filename = str(sibling.get("rfilename") or sibling.get("path") or "").lower()
        if filename.endswith(INSPECTABLE_EXTENSIONS):
            return True
    formats = text_blob(record.get("formats"), tags)
    return any(ext.strip(".") in formats for ext in INSPECTABLE_EXTENSIONS)


def score_license(tags: list[str], record: dict[str, Any]) -> tuple[str, float]:
    explicit = str(record.get("license") or "").lower().strip()
    licenses = []
    if explicit:
        licenses.append(explicit)
    for tag in tags:
        tag = str(tag).lower()
        if tag.startswith(LICENSE_TAG_PREFIX):
            licenses.append(tag.removeprefix(LICENSE_TAG_PREFIX))
    if not licenses:
        return "unknown", 0.0
    if any(license_name in KNOWN_OPEN_LICENSES for license_name in licenses):
        return "usable", 1.0
    return "review_required", 0.5


def keyword_score(blob: str, keywords: set[str]) -> float:
    hits = sum(1 for keyword in keywords if keyword in blob)
    return clamp(hits / 6)


def metadata_quality(record: dict[str, Any]) -> float:
    fields = ["id", "tags", "downloads", "likes", "lastModified", "cardData", "siblings"]
    present = sum(1 for field in fields if record.get(field) not in (None, "", [], {}))
    return round(present / len(fields), 4)


def explain_score(components: dict[str, float], inspectable: bool, license_status: str) -> str:
    top = sorted(components.items(), key=lambda item: item[1], reverse=True)[:3]
    top_text = ", ".join(f"{key}={value:.2f}" for key, value in top)
    gate = "inspectable" if inspectable else "not inspectable"
    return f"{gate}; license={license_status}; strongest components: {top_text}"
