from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

from .util import load_json, write_json

HF_DATASETS_API = "https://huggingface.co/api/datasets"


def load_catalog(path: Path | None, limit: int | None = None) -> list[dict[str, Any]]:
    if path is not None:
        data = load_json(path)
        if not isinstance(data, list):
            raise ValueError("Catalog fixture must be a JSON array of dataset records.")
        return data[:limit] if limit else data
    return list(fetch_huggingface_catalog(limit=limit))


def snapshot_catalog(records: list[dict[str, Any]], out_dir: Path, captured_at: str) -> Path:
    snapshot_path = out_dir / "snapshots" / f"huggingface_catalog_{captured_at[:10]}.json"
    write_json(snapshot_path, records)
    return snapshot_path


def fetch_huggingface_catalog(limit: int | None = None, page_size: int = 1000) -> Iterable[dict[str, Any]]:
    fetched = 0
    url = f"{HF_DATASETS_API}?{urllib.parse.urlencode({'full': 'true', 'limit': page_size})}"
    while url:
        with urllib.request.urlopen(url, timeout=60) as response:
            payload = response.read().decode("utf-8")
            page = json.loads(payload)
            if not isinstance(page, list):
                raise ValueError("Unexpected Hugging Face API response.")
            for record in page:
                yield record
                fetched += 1
                if limit is not None and fetched >= limit:
                    return
            url = _next_link(response.headers.get("Link"))


def _next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for part in link_header.split(","):
        section = part.strip()
        if 'rel="next"' not in section:
            continue
        start = section.find("<")
        end = section.find(">")
        if start != -1 and end != -1 and end > start:
            return section[start + 1 : end]
    return None
