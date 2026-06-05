"""
Detection Engine for TarkaX Failure Intelligence.
Evaluates assessment signals against the Pattern Library to detect potential failures.
"""
from typing import Dict, Any, List
from failure_intelligence.pattern_library import FAILURE_PATTERNS

def _calculate_score_100(raw_score: float) -> int:
    """Converts a raw dimension score (out of 20) to a score out of 100."""
    return int(raw_score * 5)

def _evaluate_condition(condition_key: str, condition_value: Any, signals: Dict[str, Any]) -> bool:
    """Evaluates a single trigger condition against the signals."""

    # Extract signals
    scores_100 = signals.get('scores_100', {})
    compliance_risk_flag = signals.get('compliance_risk_flag', False)
    contradictions_exist = len(signals.get('contradictions', [])) > 0
    missing_data_exist = len(signals.get('missing_data_flags', [])) > 0

    if condition_key == "governance_score_threshold":
        return scores_100.get('governance', 100) <= condition_value
    elif condition_key == "governance_score_low":
        return scores_100.get('governance', 100) <= condition_value

    elif condition_key == "awareness_score_high":
        return scores_100.get('awareness', 0) >= condition_value
    elif condition_key == "awareness_score_low":
        return scores_100.get('awareness', 100) <= condition_value

    elif condition_key == "adoption_score_low":
        return scores_100.get('adoption', 100) <= condition_value
    elif condition_key == "adoption_score_moderate":
        return scores_100.get('adoption', 0) >= condition_value
    elif condition_key == "adoption_score_high":
        return scores_100.get('adoption', 0) >= condition_value

    elif condition_key == "integration_score_low":
        return scores_100.get('integration', 100) <= condition_value

    elif condition_key == "roi_score_low":
        return scores_100.get('roi', 100) <= condition_value

    elif condition_key == "contradictions_exist":
        return contradictions_exist == condition_value

    elif condition_key == "compliance_risk_flag":
        return compliance_risk_flag == condition_value

    return False

def _generate_why_detected(pattern: Dict[str, Any], signals: Dict[str, Any]) -> str:
    """Generates the reasoning for why a pattern was detected based on signals."""
    scores_100 = signals.get('scores_100', {})
    reasons = []

    for condition_key, condition_value in pattern['trigger_conditions'].items():
        if condition_key == "governance_score_threshold" or condition_key == "governance_score_low":
            reasons.append(f"Governance score is critically low ({scores_100.get('governance', 0)}/100).")
        elif condition_key == "awareness_score_high":
            reasons.append(f"Awareness score is high ({scores_100.get('awareness', 0)}/100).")
        elif condition_key == "awareness_score_low":
            reasons.append(f"Awareness score is low ({scores_100.get('awareness', 0)}/100).")
        elif condition_key == "adoption_score_low":
            reasons.append(f"Adoption score is low ({scores_100.get('adoption', 0)}/100).")
        elif condition_key == "adoption_score_moderate" or condition_key == "adoption_score_high":
            reasons.append(f"Adoption score is significant ({scores_100.get('adoption', 0)}/100).")
        elif condition_key == "integration_score_low":
            reasons.append(f"Integration score is critically low ({scores_100.get('integration', 0)}/100).")
        elif condition_key == "roi_score_low":
            reasons.append(f"ROI measurement score is critically low ({scores_100.get('roi', 0)}/100).")
        elif condition_key == "contradictions_exist":
            reasons.append("Contradictory signals were detected in the assessment.")
        elif condition_key == "compliance_risk_flag":
            flags = signals.get('compliance_risk_reasons', [])
            reason_str = "Immediate compliance risk flagged"
            if flags:
                reason_str += f" ({', '.join(flags)})"
            reasons.append(reason_str + ".")

    return " ".join(reasons)

def _calculate_confidence(pattern: Dict[str, Any], signals: Dict[str, Any]) -> int:
    """
    Calculates a simple deterministic confidence score.
    Starts high if all conditions met, slightly modulated by overall evidence confidence.
    """
    base_confidence = signals.get('confidence_index', 100)

    # If the pattern is purely compliance or contradiction driven, confidence is high
    if "compliance_risk_flag" in pattern['trigger_conditions'] or "contradictions_exist" in pattern['trigger_conditions']:
        return max(85, base_confidence)

    return base_confidence

def detect_failure_patterns(raw_scores: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detects failure patterns based on raw assessment scores.
    Returns the top 5 most relevant patterns.
    """
    # Prepare signals
    dimensions = raw_scores.get('dimensions', {})
    scores_100 = {k: _calculate_score_100(v) for k, v in dimensions.items()}

    signals = {
        'scores_100': scores_100,
        'compliance_risk_flag': raw_scores.get('compliance_risk_flag', False),
        'compliance_risk_reasons': raw_scores.get('compliance_risk_reasons', []),
        'contradictions': raw_scores.get('contradictions', []),
        'missing_data_flags': raw_scores.get('missing_data_flags', []),
        'confidence_index': raw_scores.get('confidence_index', 100)
    }

    detected_patterns = []

    for pattern in FAILURE_PATTERNS:
        # Check if all triggers are met
        triggers_met = True
        for cond_key, cond_val in pattern['trigger_conditions'].items():
            if not _evaluate_condition(cond_key, cond_val, signals):
                triggers_met = False
                break

        if triggers_met:
            confidence = _calculate_confidence(pattern, signals)
            why_detected = _generate_why_detected(pattern, signals)

            detected_patterns.append({
                "pattern": pattern['name'],
                "severity": pattern['severity'],
                "confidence": confidence,
                "why_detected": why_detected,
                "root_causes": pattern['root_causes'],
                "consequences": pattern['consequences'],
                "recommended_actions": pattern['interventions']
            })

    # Sort and take top 5
    # Severity ranking: Critical > Major > Moderate
    severity_rank = {"Critical": 3, "Major": 2, "Moderate": 1}

    detected_patterns.sort(key=lambda x: (severity_rank.get(x['severity'], 0), x['confidence']), reverse=True)

    return detected_patterns[:5]
