from __future__ import annotations

import re

from .taxonomy import PROCESS_NODES


PROCESS_KEYWORDS = {
    "process:finance:vendor_invoice_matching": ["finance", "invoice", "tax", "erp", "reconciliation", "audit"],
    "process:hr:employee_service_intake": ["hr", "employee", "payroll", "benefits", "policy"],
    "process:procurement:vendor_onboarding": ["procurement", "vendor", "purchase", "supplier", "contract"],
    "process:customer_support:ticket_triage": ["customer", "support", "ticket", "crm", "case"],
    "process:it:incident_response": ["it", "incident", "security", "alert", "operations"],
    "process:legal:contract_review": ["legal", "contract", "clause", "compliance", "review"],
}

PROCESS_TITLES = {node["process_id"]: node["title"] for node in PROCESS_NODES}


def classify_process_sample(normalized_text: str) -> dict[str, object]:
    text = normalized_text.lower()
    ranked = []
    for process_id, keywords in PROCESS_KEYWORDS.items():
        hits = [keyword for keyword in keywords if keyword_matches(text, keyword)]
        ranked.append((process_id, hits))
    ranked.sort(key=lambda item: (len(item[1]), item[0]), reverse=True)

    primary_id, primary_hits = ranked[0]
    secondary_id, secondary_hits = ranked[1]
    secondary = secondary_id if len(secondary_hits) >= 2 and len(secondary_hits) >= len(primary_hits) - 1 else None
    confidence = min(0.95, max(0.65, 0.55 + (len(primary_hits) * 0.08)))
    if len(primary_hits) == 0:
        primary_id = "process:customer_support:ticket_triage"
        confidence = 0.65

    return {
        "process_id": primary_id,
        "process_title": PROCESS_TITLES[primary_id],
        "secondary_process": secondary,
        "confidence": round(confidence, 4),
        "reasoning": reasoning(primary_id, primary_hits, secondary),
    }


def reasoning(process_id: str, hits: list[str], secondary: str | None) -> str:
    title = PROCESS_TITLES[process_id]
    if not hits:
        return f"Defaulted to {title} because no stronger process-specific signals were present."
    signal_text = ", ".join(hits[:4])
    if secondary:
        return f"Primary match is {title} from signals: {signal_text}; secondary overlap is strong."
    return f"Primary match is {title} from signals: {signal_text}."


def keyword_matches(text: str, keyword: str) -> bool:
    if " " in keyword:
        return keyword in text
    return re.search(rf"\b{re.escape(keyword)}\b", text) is not None
