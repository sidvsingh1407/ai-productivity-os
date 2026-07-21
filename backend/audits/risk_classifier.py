import re
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from models.ai_system import AISystem
from models.risk_classification import RiskClassification
from regulation.schemas import SearchRequest
from regulation.service import RegulationService
from citations.service import CitationFormatterService

# High-Risk Domains (Annex III) keywords
HIGH_RISK_DOMAINS = {
    "biometric identification": ["biometric identification"],
    "critical infrastructure": ["critical infrastructure"],
    "education/vocational training": ["education", "vocational training"],
    "employment/worker management": ["employment", "worker management", "hiring", "recruitment"],
    "access to essential services": ["credit", "insurance", "public benefits", "essential services"],
    "law enforcement": ["law enforcement"],
    "migration/asylum/border control": ["migration", "asylum", "border control"],
    "justice administration": ["justice administration", "justice"],
    "democratic processes": ["democratic processes", "election"]
}

# Personal Data keywords
PERSONAL_DATA_KEYWORDS = [
    "personal", "pii", "user data", "customer data", "employee data", "health", "medical",
    "biometric", "financial", "location", "demographic"
]

def contains_keyword(text: str, keywords: List[str]) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)

def processes_personal_data(system: AISystem) -> bool:
    purpose = system.purpose or ""
    if contains_keyword(purpose, PERSONAL_DATA_KEYWORDS):
        return True

    for dtype in system.data_types:
        if contains_keyword(dtype, PERSONAL_DATA_KEYWORDS):
            return True

    return False

def check_unacceptable_risk(purpose: str, data_types: List[str]) -> bool:
    text_to_check = purpose.lower()
    for dtype in data_types:
        text_to_check += " " + dtype.lower()

    if "social scoring" in text_to_check:
        return True

    if "subliminal manipulation" in text_to_check:
        return True

    if "real-time remote biometric identification" in text_to_check and ("law enforcement" in text_to_check or "publicly accessible space" in text_to_check):
        return True

    if "exploitation of vulnerabilities" in text_to_check and ("age" in text_to_check or "disability" in text_to_check or "socioeconomic" in text_to_check):
        return True

    return False

def check_high_risk_domains(purpose: str, data_types: List[str]) -> List[str]:
    matched_domains = []

    text_to_check = purpose.lower()
    for dtype in data_types:
        text_to_check += " " + dtype.lower()

    for domain, keywords in HIGH_RISK_DOMAINS.items():
        if any(kw.lower() in text_to_check for kw in keywords):
            matched_domains.append(domain)

    return matched_domains

async def fetch_citation(db: AsyncSession, query_str: str) -> str:
    req = SearchRequest(query=query_str, k=1)
    results = await RegulationService().search(db, req)

    if not results:
        return "Source: EU AI Act [unspecified section]"

    citations = CitationFormatterService().format_citations(results)
    if citations:
        return citations[0].citation
    return "Source: EU AI Act [unspecified section]"

async def classify_system(system: AISystem, db: AsyncSession, audit_id: str) -> RiskClassification:
    purpose = system.purpose or ""
    data_types = system.data_types or []
    decision_making_role = system.decision_making_role or ""

    # Check Unacceptable Risk First
    if check_unacceptable_risk(purpose, data_types):
        return RiskClassification(
            audit_id=audit_id,
            ai_system_id=system.id,
            risk_level="unacceptable",
            matched_category=None,
            rationale=f"System matches prohibited practices criteria.",
            citation_reference=await fetch_citation(db, "EU AI Act Article 5 prohibited practices"),
            requires_human_review=False
        )

    matched_domains = check_high_risk_domains(purpose, data_types)

    is_automated = "fully automated" in decision_making_role.lower() and "no human review" in decision_making_role.lower()
    has_personal_data = processes_personal_data(system)

    # Check High Risk Domains
    if len(matched_domains) == 1:
        domain = matched_domains[0]
        return RiskClassification(
            audit_id=audit_id,
            ai_system_id=system.id,
            risk_level="high_risk",
            matched_category=domain,
            rationale=f"System purpose or data types match the high-risk domain: {domain}. Decision role context: {decision_making_role}.",
            citation_reference=await fetch_citation(db, f"EU AI Act Annex III {domain}"),
            requires_human_review=False
        )
    elif len(matched_domains) > 1:
         return RiskClassification(
            audit_id=audit_id,
            ai_system_id=system.id,
            risk_level="ambiguous",
            matched_category=None,
            rationale=f"System matches multiple conflicting high-risk domains: {', '.join(matched_domains)}. Requires human review to determine primary categorization.",
            citation_reference=await fetch_citation(db, "EU AI Act Annex III overview"),
            requires_human_review=True
        )

    if len(purpose.split()) <= 1 and not data_types:
        return RiskClassification(
            audit_id=audit_id,
            ai_system_id=system.id,
            risk_level="ambiguous",
            matched_category=None,
            rationale="System purpose is too vague and lacks data type context to confidently determine risk classification.",
            citation_reference=await fetch_citation(db, "EU AI Act Annex III overview"),
            requires_human_review=True
        )

    if has_personal_data:
        if is_automated:
            return RiskClassification(
                audit_id=audit_id,
                ai_system_id=system.id,
                risk_level="high_risk",
                matched_category=None,
                rationale="System processes personal data and utilizes fully automated decision making with no human review, escalating risk.",
                citation_reference=await fetch_citation(db, "EU AI Act Annex III high risk automated decision-making"),
                requires_human_review=False
            )
        else:
             return RiskClassification(
                audit_id=audit_id,
                ai_system_id=system.id,
                risk_level="limited_risk",
                matched_category=None,
                rationale="System processes personal data but is not fully automated or does not lack human review.",
                citation_reference=await fetch_citation(db, "EU AI Act limited risk transparency obligations Article 50"),
                requires_human_review=False
            )

    return RiskClassification(
        audit_id=audit_id,
        ai_system_id=system.id,
        risk_level="minimal_risk",
        matched_category=None,
        rationale="System does not match any high-risk domains and does not process personal data.",
        citation_reference=await fetch_citation(db, "EU AI Act minimal risk voluntary codes of conduct"),
        requires_human_review=False
    )
