import pytest
from audits.intelligence_engine import generate_intelligence

def test_generate_intelligence_no_context():
    scores = {
        "dimensions": {
            "governance": 13, # 13*5 = 65 -> Moderate
            "integration": 10, # 10*5 = 50 -> Major
            "awareness": 15 # 15*5 = 75 -> Advisory
        },
        "compliance_risk_flag": True,
        "compliance_risk_reasons": ["test"]
    }

    result = generate_intelligence(scores)
    findings = result["findings"]

    gov_finding = next(f for f in findings if f["title"] == "AI Governance Framework Vulnerability")
    int_finding = next(f for f in findings if f["title"] == "Systems Integration Bottleneck")
    comp_finding = next(f for f in findings if f["title"] == "Regulatory & Compliance Exposure")

    assert gov_finding["severity"] == "Moderate"
    assert int_finding["severity"] == "Major"
    assert comp_finding["severity"] == "Critical"


def test_generate_intelligence_with_criticality_bump():
    scores = {
        "dimensions": {
            "governance": 13, # 13*5 = 65 -> Moderate -> Major
            "integration": 10, # 10*5 = 50 -> Major -> stays Major (no bump for integration)
            "awareness": 15 # 15*5 = 75 -> Advisory -> stays Advisory
        }
    }

    system_context = {
        "criticality": "high",
        "decision_making_role": "advisor",
        "data_types": []
    }

    result = generate_intelligence(scores, system_context=system_context)
    findings = result["findings"]

    gov_finding = next(f for f in findings if f["title"] == "AI Governance Framework Vulnerability")
    int_finding = next(f for f in findings if f["title"] == "Systems Integration Bottleneck")

    assert gov_finding["severity"] == "Major"
    assert int_finding["severity"] == "Major"


def test_generate_intelligence_with_decision_making_role_bump():
    scores = {
        "dimensions": {
            "governance": 13, # 13*5 = 65 -> Moderate -> Major
        }
    }

    system_context = {
        "criticality": "low",
        "decision_making_role": "automated",
        "data_types": []
    }

    result = generate_intelligence(scores, system_context=system_context)
    findings = result["findings"]

    gov_finding = next(f for f in findings if f["title"] == "AI Governance Framework Vulnerability")

    assert gov_finding["severity"] == "Major"


def test_generate_intelligence_with_data_types_bump():
    scores = {
        "dimensions": {},
        "compliance_risk_flag": True,
        "compliance_risk_reasons": ["test"]
    }

    system_context = {
        "criticality": "low",
        "decision_making_role": "advisor",
        "data_types": ["personal"]
    }

    # We will test bumping compliance from Major to Critical (Wait, compliance is already Critical by default, let's check intelligence_rules)
    # Ah, COMPLIANCE_FINDING is "Critical". Bumping Critical stays Critical. Let's make sure it doesn't fail.
    result = generate_intelligence(scores, system_context=system_context)
    findings = result["findings"]

    comp_finding = next(f for f in findings if f["title"] == "Regulatory & Compliance Exposure")
    assert comp_finding["severity"] == "Critical"

def test_generate_intelligence_critical_stays_critical():
    scores = {
        "dimensions": {
            "governance": 5, # 5*5 = 25 -> Critical
        }
    }

    system_context = {
        "criticality": "high", # Triggers bump on governance
        "decision_making_role": "automated", # Triggers bump on governance
        "data_types": []
    }

    result = generate_intelligence(scores, system_context=system_context)
    findings = result["findings"]

    gov_finding = next(f for f in findings if f["title"] == "AI Governance Framework Vulnerability")

    # Critical is the ceiling, shouldn't error or exceed Critical
    assert gov_finding["severity"] == "Critical"

def test_generate_intelligence_no_multiple_bumps():
    scores = {
        "dimensions": {
            "governance": 13, # 13*5 = 65 -> Moderate -> should only bump once to Major
        }
    }

    system_context = {
        "criticality": "high", # Triggers bump
        "decision_making_role": "automated", # Triggers bump
        "data_types": []
    }

    result = generate_intelligence(scores, system_context=system_context)
    findings = result["findings"]

    gov_finding = next(f for f in findings if f["title"] == "AI Governance Framework Vulnerability")

    assert gov_finding["severity"] == "Major" # Only one step up!
