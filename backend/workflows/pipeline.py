import json
import os
import hashlib
from typing import Dict, Any, List

# To faithfully port the pipeline we use logic derived from awde_kg
from .awde_kg.config import BuildConfig
from .awde_kg.scoring import score_record
from .awde_kg.classifier import classify_process_sample
from .awde_kg.diagnostic import diagnose_workflow_friction
from .awde_kg.capability_mapper import map_ai_capability
from .awde_kg.architect import generate_automation_blueprint
from .awde_kg.graph import infer_industry_variant, text_blob
from .awde_kg.blueprint_validator import validate_blueprint_json

def get_fixture_path(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "fixtures", filename)

def load_catalog(limit: int = None) -> List[Dict[str, Any]]:
    path = get_fixture_path("catalog.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if limit:
            data = data[:limit]
        return data

def load_samples(repo_id: str) -> List[Dict[str, Any]]:
    samples_dir = get_fixture_path("samples")
    fixture = os.path.join(samples_dir, f"{repo_id.replace('/', '__')}.jsonl")
    if os.path.exists(fixture):
        rows = []
        with open(fixture, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows
    return []

def metadata_example(record: dict, index: int) -> dict:
    return {
        "split": "metadata",
        "text": text_blob(record.get("id"), record.get("cardData"), record.get("description"), record.get("tags")),
        "index": index,
        "source_kind": "metadata_derived",
    }

def process_example(record: Dict[str, Any], example: Dict[str, Any], config: BuildConfig) -> Dict[str, Any]:
    normalized = text_blob(example.get("text"), example.get("input"), example.get("output"), example)
    process_classification = classify_process_sample(normalized)
    friction_diagnostic = diagnose_workflow_friction(normalized)
    capability_mapping = map_ai_capability(
        str(process_classification["process_title"]),
        str(friction_diagnostic["cognitive_friction"]),
    )
    confidence = max(config.confidence_floor, min(0.95, record.get("enterprise_relevance_score", 0.0) + 0.05))

    return {
        "normalized_text": normalized[:2000],
        "process_classification": process_classification,
        "friction_diagnostic": friction_diagnostic,
        "capability_mapping": capability_mapping,
        "cognitive_friction": friction_diagnostic["cognitive_friction"],
        "hitl_need": friction_diagnostic["hitl_need"],
        "confidence": round(confidence, 4),
        "manual_review_required": confidence < config.confidence_floor,
    }

def blueprint_from_example(example: Dict[str, Any], config: BuildConfig) -> Dict[str, Any]:
    process_id = example["process_classification"]["process_id"]
    industry_variant = infer_industry_variant(example["normalized_text"])
    mapped_capability_id = example["capability_mapping"]["capability_id"]

    raw_blueprint = generate_automation_blueprint(
        process_title=str(example["process_classification"]["process_title"]),
        cognitive_friction=str(example["cognitive_friction"]),
        capability_id=str(mapped_capability_id),
        hitl_need=str(example["hitl_need"]),
        confidence=float(example["confidence"]),
    )["blueprint"]

    # Run blueprint validation/correction
    validation = validate_blueprint_json(raw_blueprint)
    blueprint_contract = validation["corrected_blueprint"] if not validation["valid"] else raw_blueprint

    automation_tier = str(blueprint_contract["automation_tier"])
    confidence = example["confidence"]

    return {
        "process_id": process_id,
        "automation_tier": automation_tier,
        "industry_variant": industry_variant,
        "confidence": confidence,
        "manual_review_required": confidence < 0.65,
        "blueprint_data": blueprint_contract,
        "merged": False
    }

def merge_blueprints(blueprints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged_map = {}
    for bp in blueprints:
        identity = f"{bp['process_id']}|{bp['automation_tier']}|{bp.get('industry_variant') or 'none'}"
        existing = merged_map.get(identity)
        if existing is None:
            merged_map[identity] = bp
        else:
            existing["confidence"] = max(existing["confidence"], bp["confidence"])
            existing["merged"] = True
    return list(merged_map.values())

def run_pipeline(input_config: dict) -> dict:
    mode = input_config.get("mode", "fixture")

    if mode == "live":
        raise NotImplementedError("Live mode not implemented yet")

    target_min = input_config.get("target_min", 500)
    target_max = input_config.get("target_max", 1000)
    industry_filter = input_config.get("industry_filter")

    config = BuildConfig(target_min=target_min, target_max=target_max)
    records = load_catalog()

    # Step 1: Score & Filter
    selected_records = []
    for record in records:
        scored = score_record(record, config)
        if not scored["sample_inspectability"]:
            continue
        if scored["enterprise_relevance_score"] < config.dataset_score_floor:
            continue
        record.update(scored)
        selected_records.append(record)

    selected_records.sort(
        key=lambda item: (
            item["enterprise_relevance_score"],
            item.get("downloads") or 0,
            item.get("likes") or 0,
            item.get("id") or "",
        ),
        reverse=True,
    )
    selected_records = selected_records[:target_max]

    all_blueprints = []
    process_ids = set()
    friction_patterns = set()
    capabilities = set()

    # Step 2: Extract Examples and Process
    for record in selected_records:
        samples = load_samples(record["id"])
        examples = samples[:config.samples_per_repo_max] if samples else [metadata_example(record, i) for i in range(config.samples_per_repo_min)]

        for ex in examples:
            processed_ex = process_example(record, ex, config)

            # Apply Industry filter if requested
            industry_variant = infer_industry_variant(processed_ex["normalized_text"])
            if industry_filter and industry_variant != industry_filter:
                continue

            process_ids.add(processed_ex["process_classification"]["process_id"])
            friction_patterns.add(processed_ex["cognitive_friction"])
            capabilities.add(processed_ex["capability_mapping"]["capability_id"])

            bp = blueprint_from_example(processed_ex, config)
            all_blueprints.append(bp)

    # Step 3: Merge Duplicates
    merged_blueprints = merge_blueprints(all_blueprints)

    return {
        "blueprints": merged_blueprints,
        "process_count": len(process_ids),
        "friction_patterns": list(friction_patterns),
        "capabilities": list(capabilities)
    }
