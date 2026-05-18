from __future__ import annotations

import argparse
from pathlib import Path

from .catalog import load_catalog, snapshot_catalog
from .config import BuildConfig
from .graph import build_graph
from .scoring import select_records
from .util import utc_now_iso, write_json
from .validate import ValidationError, validate_graph


def main() -> None:
    parser = argparse.ArgumentParser(prog="awde_kg")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build graph JSONL files")
    build.add_argument("--catalog", type=Path, help="Optional local Hugging Face catalog fixture JSON")
    build.add_argument("--samples", type=Path, help="Optional directory of repo sample JSONL files")
    build.add_argument("--out", type=Path, default=Path("data/graph"))
    build.add_argument("--limit", type=int, help="Optional catalog read limit")
    build.add_argument("--target-min", type=int, default=500)
    build.add_argument("--target-max", type=int, default=1000)
    build.add_argument("--samples-min", type=int, default=10)
    build.add_argument("--samples-max", type=int, default=20)

    validate = subparsers.add_parser("validate", help="Validate graph JSONL files")
    validate.add_argument("--graph", type=Path, default=Path("data/graph"))
    validate.add_argument("--target-min", type=int, default=500)
    validate.add_argument("--target-max", type=int, default=1000)

    args = parser.parse_args()
    if args.command == "build":
        run_build(args)
    elif args.command == "validate":
        run_validate(args)


def run_build(args: argparse.Namespace) -> None:
    config = BuildConfig(
        target_min=args.target_min,
        target_max=args.target_max,
        samples_per_repo_min=args.samples_min,
        samples_per_repo_max=args.samples_max,
    )
    run_at = utc_now_iso()
    records = load_catalog(args.catalog, limit=args.limit)
    snapshot_path = snapshot_catalog(records, args.out, run_at)
    selected = select_records(records, config)
    counts = build_graph(selected, args.out, args.samples, config, run_at=run_at)
    manifest = {
        "run_at": run_at,
        "catalog_snapshot": str(snapshot_path),
        "catalog_records_seen": len(records),
        "selected_records": len(selected),
        "target_min": config.target_min,
        "target_max": config.target_max,
        "dataset_score_floor": config.dataset_score_floor,
        "confidence_floor": config.confidence_floor,
        "ranking_weights": config.ranking_weights,
        "counts": counts,
    }
    write_json(args.out / "manifest.json", manifest)
    print(f"Built graph at {args.out} with {counts}")


def run_validate(args: argparse.Namespace) -> None:
    try:
        warnings = validate_graph(args.graph, args.target_min, args.target_max)
    except ValidationError as error:
        raise SystemExit(f"Validation failed: {error}") from error
    for warning in warnings:
        print(f"Warning: {warning}")
    print(f"Graph validation passed for {args.graph}")
