from __future__ import annotations

from pathlib import Path
from typing import Any

from .blueprint_validator import validate_blueprint_json
from .config import (
    AUTOMATION_TIERS,
    BLUEPRINT_STATUSES,
    CONFIDENCE_FLOOR,
    EDGE_TYPES,
    FAILURE_SIGNAL_TYPES,
    IMPLEMENTATION_OUTCOMES,
)
from .capability_mapper import ALLOWED_CAPABILITY_TYPES, AUTOMATION_POTENTIALS
from .diagnostic import ALLOWED_FRICTION_SEVERITIES, ALLOWED_FRICTION_TYPES, ALLOWED_HITL_NEEDS
from .util import read_jsonl


class ValidationError(Exception):
    pass


def validate_graph(graph_dir: Path, target_min: int = 500, target_max: int = 1000) -> list[str]:
    warnings: list[str] = []
    datasets = read_jsonl(graph_dir / "nodes.datasets.jsonl")
    examples = read_jsonl(graph_dir / "nodes.examples.jsonl")
    processes = read_jsonl(graph_dir / "nodes.processes.jsonl")
    frictions = read_jsonl(graph_dir / "nodes.friction_patterns.jsonl")
    capabilities = read_jsonl(graph_dir / "nodes.capabilities.jsonl")
    blueprints = read_jsonl(graph_dir / "nodes.blueprints.jsonl")
    implementations = read_jsonl(graph_dir / "nodes.implementations.jsonl")
    edges = read_jsonl(graph_dir / "edges.jsonl")

    selected_datasets = [row for row in datasets if row.get("selected_for_graph") is True and row.get("status") != "archived"]
    if not target_min <= len(selected_datasets) <= target_max:
        warnings.append(f"selected dataset count {len(selected_datasets)} is outside target range {target_min}-{target_max}")

    node_ids = set()
    node_ids.update(row["dataset_id"] for row in datasets)
    node_ids.update(row["example_id"] for row in examples)
    node_ids.update(row["process_id"] for row in processes)
    node_ids.update(row["friction_id"] for row in frictions)
    node_ids.update(row["capability_id"] for row in capabilities)
    node_ids.update(row["blueprint_id"] for row in blueprints)

    validate_datasets(datasets)
    validate_examples(examples)
    validate_processes(processes)
    validate_blueprints(blueprints, node_ids)
    validate_implementations(implementations, {item["blueprint_id"] for item in blueprints})
    validate_edges(edges, node_ids)
    return warnings


def validate_datasets(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        if row.get("status") == "archived":
            if row.get("selected_for_graph") is not False:
                raise ValidationError(f"{row['dataset_id']} is archived but still selected")
            continue
        if row["sample_inspectability"] is not True:
            raise ValidationError(f"{row['dataset_id']} failed inspectability gate but was selected")
        if row["enterprise_relevance_score"] < 0.70:
            raise ValidationError(f"{row['dataset_id']} is below dataset score floor")
        if row["license_status"] == "unknown":
            raise ValidationError(f"{row['dataset_id']} has unknown license in selected graph")


def validate_examples(rows: list[dict[str, Any]]) -> None:
    required = {
        "example_id",
        "source_repo_id",
        "split",
        "row_hash",
        "normalized_text",
        "detected_process",
        "process_classification",
        "friction_diagnostic",
        "capability_mapping",
        "cognitive_friction",
        "friction_severity",
        "mechanical_friction",
        "hitl_need",
        "confidence",
    }
    for row in rows:
        require_fields(row, required, "example")
        validate_process_classification(row["process_classification"])
        validate_friction_diagnostic(row["friction_diagnostic"])
        validate_capability_mapping(row["capability_mapping"])
        if row["cognitive_friction"] != row["friction_diagnostic"]["cognitive_friction"]:
            raise ValidationError("example cognitive_friction must mirror friction_diagnostic")
        if row["hitl_need"] != row["friction_diagnostic"]["hitl_need"]:
            raise ValidationError("example hitl_need must mirror friction_diagnostic")
        validate_confidence(row)


def validate_processes(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        variants = row.get("industry_variants", [])
        if len(variants) > 10:
            raise ValidationError(f"{row['process_id']} has more than 10 embedded industry variants")
        for variant in variants:
            require_fields(
                variant,
                {"industry_tag", "delta_tools", "delta_hitl_weight", "compliance_flags", "confidence"},
                "industry_variant",
            )
            validate_confidence(variant)


def validate_process_classification(row: dict[str, Any]) -> None:
    require_fields(
        row,
        {"process_id", "process_title", "secondary_process", "confidence", "reasoning"},
        "process_classification",
    )
    validate_confidence(row)
    if not isinstance(row["reasoning"], str) or not row["reasoning"]:
        raise ValidationError("process_classification reasoning must be a non-empty string")


def validate_friction_diagnostic(row: dict[str, Any]) -> None:
    require_fields(
        row,
        {"cognitive_friction", "friction_severity", "mechanical_friction", "hitl_need", "confidence"},
        "friction_diagnostic",
    )
    if row["cognitive_friction"] not in ALLOWED_FRICTION_TYPES:
        raise ValidationError("friction_diagnostic cognitive_friction has invalid value")
    if row["friction_severity"] not in ALLOWED_FRICTION_SEVERITIES:
        raise ValidationError("friction_diagnostic friction_severity has invalid value")
    if row["hitl_need"] not in ALLOWED_HITL_NEEDS:
        raise ValidationError("friction_diagnostic hitl_need has invalid value")
    if not isinstance(row["mechanical_friction"], str):
        raise ValidationError("friction_diagnostic mechanical_friction must be a string")
    validate_confidence(row)


def validate_capability_mapping(row: dict[str, Any]) -> None:
    require_fields(
        row,
        {"capability_id", "capability_type", "automation_potential", "reasoning", "confidence"},
        "capability_mapping",
    )
    if row["capability_type"] not in ALLOWED_CAPABILITY_TYPES:
        raise ValidationError("capability_mapping capability_type has invalid value")
    if row["capability_id"] != f"capability:{row['capability_type']}":
        raise ValidationError("capability_mapping capability_id must match capability_type")
    if row["automation_potential"] not in AUTOMATION_POTENTIALS:
        raise ValidationError("capability_mapping automation_potential has invalid value")
    if not isinstance(row["reasoning"], str) or not row["reasoning"]:
        raise ValidationError("capability_mapping reasoning must be a non-empty string")
    validate_confidence(row)


def validate_blueprints(rows: list[dict[str, Any]], node_ids: set[str]) -> None:
    required = {
        "blueprint_id",
        "version",
        "status",
        "last_validated",
        "superseded_by",
        "process_id",
        "title",
        "diagnosis",
        "tool_stack",
        "orchestration_pipeline",
        "hitl_checkpoint",
        "automation_tier",
        "estimated_time_saved",
        "blueprint_contract",
        "industry_variant",
        "confidence",
        "source_evidence_ids",
        "implementation_count",
        "avg_actual_time_saved",
        "user_reported_accuracy",
        "failure_signals",
    }
    identities: set[tuple[str, str, str | None]] = set()
    for row in rows:
        require_fields(row, required, "blueprint")
        if row["status"] not in BLUEPRINT_STATUSES:
            raise ValidationError(f"{row['blueprint_id']} has invalid status")
        if row["automation_tier"] not in AUTOMATION_TIERS:
            raise ValidationError(f"{row['blueprint_id']} has invalid automation_tier")
        validate_confidence(row)
        identity = (row["process_id"], row["automation_tier"], row["industry_variant"])
        if identity in identities:
            raise ValidationError(f"duplicate blueprint identity was not merged: {identity}")
        identities.add(identity)
        if row["process_id"] not in node_ids:
            raise ValidationError(f"{row['blueprint_id']} references missing process")
        for evidence_id in row["source_evidence_ids"]:
            if evidence_id not in node_ids:
                raise ValidationError(f"{row['blueprint_id']} references missing evidence {evidence_id}")
        validate_tool_stack(row)
        validate_pipeline(row)
        validate_blueprint_contract(row)
        validate_failure_signals(row)


def validate_tool_stack(row: dict[str, Any]) -> None:
    if not isinstance(row["tool_stack"], list) or not row["tool_stack"]:
        raise ValidationError(f"{row['blueprint_id']} tool_stack must be a non-empty list")
    for tool in row["tool_stack"]:
        require_fields(tool, {"capability_id", "tool_name", "role", "open_source", "fallback"}, "tool_stack")
        if not isinstance(tool["open_source"], bool):
            raise ValidationError(f"{row['blueprint_id']} tool_stack open_source must be boolean")


def validate_pipeline(row: dict[str, Any]) -> None:
    steps = row["orchestration_pipeline"]
    if not isinstance(steps, list) or not steps:
        raise ValidationError(f"{row['blueprint_id']} orchestration_pipeline must be non-empty")
    if len(steps) > 5:
        raise ValidationError(f"{row['blueprint_id']} orchestration_pipeline must have at most 5 steps")
    expected = 1
    for step in steps:
        require_fields(step, {"step", "action", "capability_id", "input", "output", "hitl_required"}, "pipeline_step")
        if step["step"] != expected:
            raise ValidationError(f"{row['blueprint_id']} pipeline steps must be ordered from 1")
        if not isinstance(step["hitl_required"], bool):
            raise ValidationError(f"{row['blueprint_id']} hitl_required must be boolean")
        expected += 1
    if row["hitl_checkpoint"] is not None and not any(step["hitl_required"] for step in steps):
        raise ValidationError(f"{row['blueprint_id']} hitl_checkpoint requires at least one HITL pipeline step")
    if row["hitl_checkpoint"] is None and any(step["hitl_required"] for step in steps):
        raise ValidationError(f"{row['blueprint_id']} HITL pipeline step requires hitl_checkpoint")


def validate_blueprint_contract(row: dict[str, Any]) -> None:
    contract = row["blueprint_contract"]
    require_fields(
        contract,
        {
            "title",
            "automation_tier",
            "orchestration_pipeline",
            "hitl_checkpoint",
            "estimated_time_saved",
            "confidence",
        },
        "blueprint_contract",
    )
    if contract["title"] != row["title"]:
        raise ValidationError(f"{row['blueprint_id']} blueprint_contract title must mirror blueprint title")
    if contract["automation_tier"] != row["automation_tier"]:
        raise ValidationError(f"{row['blueprint_id']} blueprint_contract automation_tier must mirror blueprint")
    if contract["orchestration_pipeline"] != row["orchestration_pipeline"]:
        raise ValidationError(f"{row['blueprint_id']} blueprint_contract pipeline must mirror blueprint")
    if contract["hitl_checkpoint"] != row["hitl_checkpoint"]:
        raise ValidationError(f"{row['blueprint_id']} blueprint_contract hitl_checkpoint must mirror blueprint")
    if contract["estimated_time_saved"] != row["estimated_time_saved"]:
        raise ValidationError(f"{row['blueprint_id']} blueprint_contract estimated_time_saved must mirror blueprint")
    validate_confidence(contract)
    result = validate_blueprint_json(contract)
    if not result["valid"]:
        raise ValidationError(f"{row['blueprint_id']} blueprint_contract failed strict validation: {result['errors']}")


def validate_failure_signals(row: dict[str, Any]) -> None:
    if not isinstance(row["failure_signals"], list):
        raise ValidationError(f"{row['blueprint_id']} failure_signals must be a list")
    for signal in row["failure_signals"]:
        require_fields(signal, {"reported_at", "signal_type", "description", "resolved"}, "failure_signal")
        if signal["signal_type"] not in FAILURE_SIGNAL_TYPES:
            raise ValidationError(f"{row['blueprint_id']} has invalid failure signal type")
        if not isinstance(signal["resolved"], bool):
            raise ValidationError(f"{row['blueprint_id']} failure signal resolved must be boolean")


def validate_implementations(rows: list[dict[str, Any]], blueprint_ids: set[str]) -> None:
    required = {
        "implementation_id",
        "blueprint_id",
        "industry_tag",
        "company_size_band",
        "reported_time_saved",
        "outcome",
        "timestamp",
    }
    for row in rows:
        require_fields(row, required, "implementation")
        if row["blueprint_id"] not in blueprint_ids:
            raise ValidationError(f"{row['implementation_id']} references missing blueprint")
        if row["outcome"] not in IMPLEMENTATION_OUTCOMES:
            raise ValidationError(f"{row['implementation_id']} has invalid outcome")


def validate_edges(rows: list[dict[str, Any]], node_ids: set[str]) -> None:
    required = {"edge_id", "edge_type", "source_node_id", "target_node_id", "confidence", "evidence_ids", "created_at"}
    for row in rows:
        require_fields(row, required, "edge")
        if row["edge_type"] not in EDGE_TYPES:
            raise ValidationError(f"{row['edge_id']} has invalid edge type")
        if row["source_node_id"] not in node_ids:
            raise ValidationError(f"{row['edge_id']} references missing source {row['source_node_id']}")
        if row["target_node_id"] not in node_ids:
            raise ValidationError(f"{row['edge_id']} references missing target {row['target_node_id']}")
        validate_confidence(row)
        for evidence_id in row["evidence_ids"]:
            if evidence_id not in node_ids:
                raise ValidationError(f"{row['edge_id']} references missing evidence {evidence_id}")


def validate_confidence(row: dict[str, Any]) -> None:
    confidence = row["confidence"]
    if not isinstance(confidence, (float, int)) or not 0.0 <= confidence <= 1.0:
        raise ValidationError("confidence must be a float from 0.0 to 1.0")
    if confidence < CONFIDENCE_FLOOR and row.get("manual_review_required") is not True:
        raise ValidationError("confidence below floor requires manual_review_required=true")


def require_fields(row: dict[str, Any], fields: set[str], label: str) -> None:
    missing = [field for field in sorted(fields) if field not in row]
    if missing:
        raise ValidationError(f"{label} missing required fields: {missing}")
