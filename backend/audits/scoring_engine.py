#!/usr/bin/env python3
"""
AI Productivity Intelligence System - Scoring Engine
Calculates AI maturity scores from form responses.

Usage: python scoring_engine.py <form_response.json>
Output: Prints score breakdown and sets compliance flags
"""

import json
from typing import Dict, Any, Tuple

# Point mapping for responses (a=20, b=15, c=10, d=5, e=0)
RESPONSE_POINTS = {
    'a': 20,
    'b': 15,
    'c': 10,
    'd': 5,
    'e': 0,
    'A': 20,
    'B': 15,
    'C': 10,
    'D': 5,
    'E': 0,
}

# Question groupings by dimension
DIMENSION_QUESTIONS = {
    'awareness': ['q1_1', 'q1_2', 'q1_3'],
    'adoption': ['q2_1', 'q2_2', 'q2_3'],
    'integration': ['q3_1', 'q3_2', 'q3_3'],
    'governance': ['q4_1', 'q4_2', 'q4_3'],
    'roi': ['q5_1', 'q5_2', 'q5_3'],
}

# Compliance risk triggers (these responses indicate risk)
COMPLIANCE_RISK_RESPONSES = {
    'q4_1': ['d', 'e'],  # No policy or informal only
    'q4_2': ['d', 'e'],  # Employee discretion or no oversight
    'q4_3': ['d', 'e'],  # Unaware or no action on EU AI Act
}


def response_to_points(response: str) -> int:
    """Convert a single response to points."""
    return RESPONSE_POINTS.get(response, 0)


def calculate_dimension_score(responses: Dict[str, str], dimension: str) -> Tuple[int, bool]:
    """
    Calculate score for a single dimension.

    Returns:
        Tuple of (score, has_missing_data)
    """
    questions = DIMENSION_QUESTIONS[dimension]
    points = []

    for q in questions:
        response = responses.get(q)
        if response is not None and response.strip() != '':
            points.append(response_to_points(response))

    # Handle missing data
    if len(points) == 0:
        # All questions missing
        return 0, True
    elif len(points) == 1:
        # 2 questions missing: average the 1, multiply by 1.5
        return round(points[0] * 1.5), True
    elif len(points) == 2:
        # 1 question missing: average the 2, multiply by 1.5
        return round(sum(points) / 2 * 1.5), True
    else:
        # All 3 questions present
        return round(sum(points) / 3), False


def check_compliance_risk(responses: Dict[str, str]) -> Tuple[bool, list]:
    """
    Check if compliance risk flag should be set.

    Returns:
        Tuple of (has_risk, list of risk reasons)
    """
    risk_reasons = []

    for question, risky_responses in COMPLIANCE_RISK_RESPONSES.items():
        response = responses.get(question)
        if response in risky_responses:
            risk_reasons.append(question)

    return len(risk_reasons) > 0, risk_reasons


import re

def detect_contradictions(responses: Dict[str, str], evidence_response: Dict[str, Any] = None) -> list:
    """
    Detect contradictory responses that need manual review.

    Returns:
        List of contradiction descriptions
    """
    contradictions = []
    if evidence_response is None:
        evidence_response = {}

    # Rule 1: Governance Claim Without Evidence
    gov_claim = responses.get('q4_1', 'e').lower()
    gov_evidence = evidence_response.get('q4_1', {})
    if gov_claim in ['a', 'b'] and not gov_evidence.get('evidence_url'):
        contradictions.append("Governance policy claimed but no supporting evidence provided.")

    # Rule 2: High AI Adoption Without Evidence
    adopt_claim = responses.get('q2_1', 'e').lower()
    adopt_evidence = evidence_response.get('q2_1', {})
    if adopt_claim in ['a', 'b'] and not adopt_evidence.get('evidence_url'):
        contradictions.append("High AI adoption claimed but no supporting evidence provided.")

    # Rule 3: High Integration Without Evidence
    int_claim = responses.get('q3_1', 'e').lower()
    int_evidence = evidence_response.get('q3_1', {})
    if int_claim in ['a', 'b'] and not int_evidence.get('evidence_url'):
        contradictions.append("High workflow integration claimed but no supporting evidence provided.")

    # Rule 4: Workflow Standardization Contradiction
    std_claim = responses.get('q3_2', 'e').lower()
    std_evidence = evidence_response.get('q3_2', {})
    std_context = (std_evidence.get('evidence_context') or "").lower()
    if std_claim in ['a', 'b'] and any(word in std_context for word in ['manual', 'spreadsheet', 'excel', 'workaround']):
        contradictions.append("Standardized workflow claimed but manual workarounds referenced.")

    # Rule 5: ROI Contradiction
    roi_claim = responses.get('q5_1', 'e').lower()
    roi_evidence = evidence_response.get('q5_1', {})
    roi_context = roi_evidence.get('evidence_context') or ""
    if roi_claim in ['a', 'b'] and len(roi_context) < 30:
        contradictions.append("Strong ROI claimed without sufficient supporting explanation.")

    return contradictions


def calculate_evidence_quality_score(evidence_response: Dict[str, Any]) -> int:
    """
    Calculate the Evidence Quality Score (EQS) from 20 to 100.
    Calculates average across all provided evidence objects.
    """
    if not evidence_response:
        return 20

    scores = []
    for key, ev in evidence_response.items():
        url = ev.get('evidence_url') or ""
        context = ev.get('evidence_context') or ""

        # Split URLs by comma, newline, or semicolon
        url_list = []
        if url:
            raw_urls = re.split(r'[,\n;]', url)
            url_list = [u.strip() for u in raw_urls if u.strip()]

        has_url = len(url_list) > 0
        multiple_urls = len(url_list) >= 2
        ctx_len = len(context)

        if multiple_urls and ctx_len >= 51:
            scores.append(100) # L5
        elif has_url and ctx_len >= 51:
            scores.append(80) # L4
        elif has_url and 1 <= ctx_len <= 50:
            scores.append(60) # L3
        elif not has_url and 1 <= ctx_len <= 50:
            scores.append(40) # L2
        else:
            scores.append(20) # L1

    if not scores:
        return 20

    return round(sum(scores) / len(scores))


def calculate_confidence_index(eqs: int, missing_evidence_count: int, contradiction_count: int) -> int:
    """
    Calculate the Confidence Index based on EQS, missing evidence, and contradictions.
    """
    missing_penalty = missing_evidence_count * 5
    contradiction_penalty = contradiction_count * 10

    confidence = eqs - missing_penalty - contradiction_penalty
    return max(0, min(100, confidence))


def get_score_rating(total_score: int) -> str:
    """Get rating label for total score."""
    if total_score >= 80:
        return "AI Mature"
    elif total_score >= 60:
        return "AI Adopting"
    elif total_score >= 40:
        return "AI Emerging"
    elif total_score >= 20:
        return "AI Initial"
    else:
        return "AI Nascent"


def score_response(responses: Dict[str, str], evidence_response: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Calculate all scores from form responses.

    Args:
        responses: Dictionary of question_id -> response
        evidence_response: Optional dictionary of question_id -> evidence dict

    Returns:
        Dictionary with all scores, flags, and metadata
    """
    if evidence_response is None:
        evidence_response = {}

    result = {
        'dimensions': {},
        'total_score': 0,
        'evidence_quality_score': None,
        'confidence_index': None,
        'rating': '',
        'compliance_risk_flag': False,
        'compliance_risk_reasons': [],
        'contradictions': [],
        'missing_data_flags': [],
    }

    # Calculate each dimension
    for dimension in DIMENSION_QUESTIONS.keys():
        score, has_missing = calculate_dimension_score(responses, dimension)
        result['dimensions'][dimension] = score
        if has_missing:
            result['missing_data_flags'].append(dimension)

    # Calculate total
    result['total_score'] = sum(result['dimensions'].values())
    result['rating'] = get_score_rating(result['total_score'])

    # Check compliance risk
    has_risk, risk_reasons = check_compliance_risk(responses)
    result['compliance_risk_flag'] = has_risk
    result['compliance_risk_reasons'] = risk_reasons

    # Detect contradictions
    contradictions = detect_contradictions(responses, evidence_response)
    result['contradictions'] = contradictions

    # Calculate EQS and Confidence
    # First, calculate missing evidence count
    # Evidence should be provided for every question that was answered
    answered_questions = [k for k, v in responses.items() if v.strip() != '']
    missing_evidence_count = 0
    for q_id in answered_questions:
        ev = evidence_response.get(q_id, {})
        # If no url and no context, we consider it missing evidence object for the penalty
        if not ev.get('evidence_url') and not ev.get('evidence_context'):
            missing_evidence_count += 1

    eqs = calculate_evidence_quality_score(evidence_response)
    confidence = calculate_confidence_index(eqs, missing_evidence_count, len(contradictions))

    result['evidence_quality_score'] = eqs
    result['confidence_index'] = confidence

    return result


def load_form_responses(filepath: str) -> Dict[str, Any]:
    """Load form responses from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def format_score_report(scores: Dict[str, Any], company_name: str = "") -> str:
    """Format scores as human-readable report."""
    lines = [
        "=" * 50,
        "AI MATURITY SCORE REPORT",
        f"Company: {company_name or 'Unknown'}",
        "=" * 50,
        "",
        f"TOTAL SCORE: {scores['total_score']}/100",
        f"RATING: {scores['rating']}",
        "",
        "DIMENSION BREAKDOWN:",
        f"  Awareness:   {scores['dimensions']['awareness']}/20",
        f"  Adoption:    {scores['dimensions']['adoption']}/20",
        f"  Integration: {scores['dimensions']['integration']}/20",
        f"  Governance:  {scores['dimensions']['governance']}/20",
        f"  ROI:         {scores['dimensions']['roi']}/20",
        "",
    ]

    if scores['compliance_risk_flag']:
        lines.extend([
            "[!] COMPLIANCE RISK FLAG: TRUE",
            f"    Risk reasons: {', '.join(scores['compliance_risk_reasons'])}",
            "",
        ])

    if scores['contradictions']:
        lines.extend([
            "[!] CONTRADICTIONS DETECTED (Manual Review Needed):",
        ])
        for contradiction in scores['contradictions']:
            lines.append(f"    - {contradiction}")
        lines.append("")

    if scores['missing_data_flags']:
        lines.extend([
            "[!] MISSING DATA IN DIMENSIONS:",
        ])
        for dim in scores['missing_data_flags']:
            lines.append(f"    - {dim}")
        lines.append("")

    lines.append("=" * 50)

    return "\n".join(lines)
