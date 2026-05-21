from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .architect import generate_automation_blueprint
from .capability_mapper import map_ai_capability
from .classifier import classify_process_sample
from .config import BuildConfig
from .diagnostic import diagnose_workflow_friction
from .taxonomy import CAPABILITY_NODES, FRICTION_PATTERN_NODES, PROCESS_NODES
from .util import read_jsonl, stable_hash, text_blob, utc_now_iso, write_jsonl


def build_graph(
    selected_records: list[dict[str, Any]],
    out_dir: Path,
    samples_dir: Path | None,
    config: BuildConfig,
    run_at: str | None = None,
) -> dict[str, int]:
    run_at = run_at or utc_now_iso()
    current_dataset_nodes = [dataset_node(record, run_at) for record in selected_records]
    dataset_nodes = current_dataset_nodes + archived_dataset_nodes(out_dir, current_dataset_nodes, run_at)
    example_nodes = []
    edges = []
    blueprints_by_identity: dict[str, dict[str, Any]] = {}

    for dataset in current_dataset_nodes:
        record = next(item for item in selected_records if dataset["repo_id"] == item["id"])
        examples = sample_examples(record, samples_dir, config)
        for example in examples:
            example_node = example_to_node(record, example, run_at, config)
            process_id = example_node["process_classification"]["process_id"]
            example_nodes.append(example_node)
            edges.append(edge("HAS_SAMPLE", dataset["dataset_id"], example_node["example_id"], [example_node["example_id"]], 0.9, run_at))
            edges.append(edge("SUPPORTS_PROCESS", dataset["dataset_id"], process_id, [example_node["example_id"]], example_node["confidence"], run_at))
            friction_id = infer_friction_id(example_node["normalized_text"])
            edges.append(edge("EVIDENCES_FRICTION", example_node["example_id"], friction_id, [example_node["example_id"]], example_node["confidence"], run_at))
            blueprint = blueprint_from_example(example_node, process_id, friction_id, run_at)
            merge_blueprint(blueprints_by_identity, blueprint)

    blueprint_nodes = list(blueprints_by_identity.values())
    for blueprint in blueprint_nodes:
        edges.append(edge("GENERATES_BLUEPRINT", blueprint["process_id"], blueprint["blueprint_id"], blueprint["source_evidence_ids"], blueprint["confidence"], run_at))
        for tool in blueprint["tool_stack"]:
            edges.append(edge("REQUIRES_CAPABILITY", blueprint["blueprint_id"], tool["capability_id"], blueprint["source_evidence_ids"], blueprint["confidence"], run_at))
        if blueprint["hitl_checkpoint"] is not None:
            edges.append(edge("REQUIRES_HITL", blueprint["blueprint_id"], "capability:human_approval", blueprint["source_evidence_ids"], blueprint["confidence"], run_at))

    write_jsonl(out_dir / "nodes.datasets.jsonl", dataset_nodes)
    write_jsonl(out_dir / "nodes.examples.jsonl", example_nodes)
    write_jsonl(out_dir / "nodes.processes.jsonl", PROCESS_NODES)
    write_jsonl(out_dir / "nodes.friction_patterns.jsonl", FRICTION_PATTERN_NODES)
    write_jsonl(out_dir / "nodes.capabilities.jsonl", CAPABILITY_NODES)
    write_jsonl(out_dir / "nodes.blueprints.jsonl", blueprint_nodes)
    write_jsonl(out_dir / "nodes.implementations.jsonl", [])
    write_jsonl(out_dir / "edges.jsonl", edges)

    return {
        "datasets": len(dataset_nodes),
        "examples": len(example_nodes),
        "processes": len(PROCESS_NODES),
        "friction_patterns": len(FRICTION_PATTERN_NODES),
        "capabilities": len(CAPABILITY_NODES),
        "blueprints": len(blueprint_nodes),
        "edges": len(edges),
    }


def dataset_node(record: dict[str, Any], run_at: str) -> dict[str, Any]:
    repo_id = record["id"]
    return {
        "dataset_id": f"hf_dataset:{repo_id}",
        "node_type": "dataset",
        "repo_id": repo_id,
        "url": f"https://huggingface.co/datasets/{repo_id}",
        "license": record.get("license"),
        "license_status": record.get("license_status"),
        "tags": record.get("tags") or [],
        "downloads": record.get("downloads"),
        "likes": record.get("likes"),
        "last_modified": record.get("lastModified"),
        "modality": infer_modality(record),
        "task_categories": record.get("task_categories") or [],
        "enterprise_relevance_score": record["enterprise_relevance_score"],
        "score_components": record["score_components"],
        "score_explanation": record["score_explanation"],
        "sample_inspectability": record["sample_inspectability"],
        "selected_for_graph": record["selected_for_graph"],
        "status": record.get("status", "active"),
        "created_at": run_at,
    }


def archived_dataset_nodes(out_dir: Path, current_nodes: list[dict[str, Any]], run_at: str) -> list[dict[str, Any]]:
    previous_path = out_dir / "nodes.datasets.jsonl"
    if not previous_path.exists():
        return []
    current_ids = {node["dataset_id"] for node in current_nodes}
    archived = []
    for previous in read_jsonl(previous_path):
        if previous["dataset_id"] in current_ids:
            continue
        retained = dict(previous)
        retained["selected_for_graph"] = False
        retained["status"] = "archived"
        retained["archived_at"] = run_at
        archived.append(retained)
    return archived


def sample_examples(record: dict[str, Any], samples_dir: Path | None, config: BuildConfig) -> list[dict[str, Any]]:
    repo_id = record["id"]
    if samples_dir:
        fixture = samples_dir / f"{repo_id.replace('/', '__')}.jsonl"
        if fixture.exists():
            rows = []
            with fixture.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if line:
                        rows.append(json.loads(line))
            return rows[: config.samples_per_repo_max]
    return [metadata_example(record, index) for index in range(config.samples_per_repo_min)]


def metadata_example(record: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "split": "metadata",
        "text": text_blob(record.get("id"), record.get("cardData"), record.get("description"), record.get("tags")),
        "index": index,
        "source_kind": "metadata_derived",
    }


def example_to_node(
    record: dict[str, Any],
    example: dict[str, Any],
    run_at: str,
    config: BuildConfig,
) -> dict[str, Any]:
    normalized = text_blob(example.get("text"), example.get("input"), example.get("output"), example)
    process_classification = classify_process_sample(normalized)
    friction_diagnostic = diagnose_workflow_friction(normalized)
    capability_mapping = map_ai_capability(
        str(process_classification["process_title"]),
        str(friction_diagnostic["cognitive_friction"]),
    )
    confidence = max(config.confidence_floor, min(0.95, record["enterprise_relevance_score"] + 0.05))
    row_hash = stable_hash({"repo": record["id"], "example": example})
    return {
        "example_id": f"hf_example:{record['id']}:{example.get('split', 'unknown')}:{row_hash}",
        "node_type": "example",
        "source_repo_id": record["id"],
        "split": example.get("split", "unknown"),
        "row_hash": row_hash,
        "normalized_text": normalized[:2000],
        "detected_process": process_classification["process_id"],
        "process_classification": process_classification,
        "friction_diagnostic": friction_diagnostic,
        "capability_mapping": capability_mapping,
        "cognitive_friction": friction_diagnostic["cognitive_friction"],
        "friction_severity": friction_diagnostic["friction_severity"],
        "mechanical_friction": friction_diagnostic["mechanical_friction"],
        "hitl_need": friction_diagnostic["hitl_need"],
        "confidence": round(confidence, 4),
        "manual_review_required": confidence < config.confidence_floor,
        "created_at": run_at,
    }


def blueprint_from_example(example: dict[str, Any], process_id: str, friction_id: str, run_at: str) -> dict[str, Any]:
    industry_variant = infer_industry_variant(example["normalized_text"])
    mapped_capability_id = example["capability_mapping"]["capability_id"]
    blueprint_contract = generate_automation_blueprint(
        process_title=str(example["process_classification"]["process_title"]),
        cognitive_friction=str(example["cognitive_friction"]),
        capability_id=str(mapped_capability_id),
        hitl_need=str(example["hitl_need"]),
        confidence=float(example["confidence"]),
    )["blueprint"]
    automation_tier = str(blueprint_contract["automation_tier"])
    identity = {
        "process_id": process_id,
        "automation_tier": automation_tier,
        "industry_variant": industry_variant,
    }
    blueprint_id = f"blueprint:{stable_hash(identity)}"
    confidence = example["confidence"]
    return {
        "blueprint_id": blueprint_id,
        "node_type": "blueprint",
        "version": "1.0",
        "status": "active",
        "last_validated": run_at,
        "superseded_by": None,
        "process_id": process_id,
        "title": blueprint_contract["title"],
        "diagnosis": {
            "cognitive_friction": example["cognitive_friction"],
            "friction_severity": example["friction_severity"],
            "mechanical_friction": example["mechanical_friction"],
            "hitl_need": example["hitl_need"],
            "friction_pattern_ids": [friction_id],
        },
        "tool_stack": [
            tool_for_capability(str(mapped_capability_id)),
            {
                "capability_id": "capability:orchestration",
                "tool_name": "n8n",
                "role": "workflow_orchestration",
                "open_source": True,
                "fallback": "Make",
            },
            {
                "capability_id": "capability:human_approval",
                "tool_name": "Slack",
                "role": "approval_checkpoint",
                "open_source": False,
                "fallback": "Teams",
            },
        ],
        "orchestration_pipeline": blueprint_contract["orchestration_pipeline"],
        "hitl_checkpoint": blueprint_contract["hitl_checkpoint"],
        "automation_tier": automation_tier,
        "estimated_time_saved": blueprint_contract["estimated_time_saved"],
        "blueprint_contract": blueprint_contract,
        "industry_variant": industry_variant,
        "confidence": confidence,
        "manual_review_required": confidence < 0.65,
        "source_evidence_ids": [example["example_id"]],
        "implementation_count": 0,
        "avg_actual_time_saved": None,
        "user_reported_accuracy": None,
        "failure_signals": [],
        "merged": False,
    }


def merge_blueprint(blueprints_by_identity: dict[str, dict[str, Any]], blueprint: dict[str, Any]) -> None:
    identity = "|".join([blueprint["process_id"], blueprint["automation_tier"], blueprint["industry_variant"] or "none"])
    existing = blueprints_by_identity.get(identity)
    if existing is None:
        blueprints_by_identity[identity] = blueprint
        return
    existing["source_evidence_ids"] = sorted(set(existing["source_evidence_ids"] + blueprint["source_evidence_ids"]))
    existing["confidence"] = max(existing["confidence"], blueprint["confidence"])
    existing["merged"] = True
    pattern_ids = set(existing["diagnosis"]["friction_pattern_ids"])
    pattern_ids.update(blueprint["diagnosis"]["friction_pattern_ids"])
    existing["diagnosis"]["friction_pattern_ids"] = sorted(pattern_ids)


def edge(edge_type: str, source: str, target: str, evidence_ids: list[str], confidence: float, run_at: str) -> dict[str, Any]:
    payload = {
        "edge_type": edge_type,
        "source_node_id": source,
        "target_node_id": target,
        "evidence_ids": sorted(set(evidence_ids)),
    }
    return {
        "edge_id": f"edge:{stable_hash(payload)}",
        **payload,
        "confidence": round(confidence, 4),
        "manual_review_required": confidence < 0.65,
        "created_at": run_at,
    }


def infer_friction_id(text: str) -> str:
    if any(word in text for word in ["ticket", "routing", "priority", "triage"]):
        return "friction:cognitive:triage_and_routing"
    if any(word in text for word in ["approval", "email", "reminder", "followup"]):
        return "friction:mechanical:approval_followup"
    if any(word in text for word in ["erp", "crm", "copy", "writeback"]):
        return "friction:mechanical:system_rekeying"
    return "friction:cognitive:document_cross_reference"


def tool_for_capability(capability_id: str) -> dict[str, object]:
    tool_names = {
        "capability:document_extraction": ("Claude", "document_extraction", "Gemini"),
        "capability:classification": ("Claude", "workflow_classification", "Gemini"),
        "capability:summarization": ("Claude", "summarization", "Gemini"),
        "capability:entity_resolution": ("Claude", "entity_resolution", "rules engine"),
        "capability:decision_support": ("Claude", "decision_support", "Gemini"),
        "capability:orchestration": ("n8n", "workflow_orchestration", "Make"),
    }
    tool_name, role, fallback = tool_names.get(capability_id, ("Claude", "reasoning", "Gemini"))
    return {
        "capability_id": capability_id,
        "tool_name": tool_name,
        "role": role,
        "open_source": tool_name == "n8n",
        "fallback": fallback,
    }


def infer_industry_variant(text: str) -> str | None:
    for industry in ["healthcare", "banking", "public_sector", "regulated_enterprise"]:
        if industry.replace("_", " ") in text or industry in text:
            return industry
    return None


def infer_modality(record: dict[str, Any]) -> str:
    blob = text_blob(record.get("tags"), record.get("cardData"))
    for modality in ["text", "tabular", "document", "image", "audio", "video"]:
        if modality in blob:
            return modality
    return "unknown"


def blueprint_title(process_id: str, industry_variant: str | None) -> str:
    base = process_id.split(":")[-1].replace("_", " ").title()
    if industry_variant:
        return f"{base} Blueprint ({industry_variant.replace('_', ' ').title()})"
    return f"{base} Blueprint"
