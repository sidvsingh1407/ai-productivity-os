import pytest
from backend.prompt_intelligence.context_classifier import ContextClassifier
from backend.prompt_intelligence.diagnosis_engine import DiagnosisEngine
from backend.prompt_intelligence.context_rules import FALLBACK_CONTEXT

def test_context_classifier_process_automation():
    prompt = "automate the workflow using a trigger"
    result = ContextClassifier.classify(prompt)
    assert result["context"] == "Process Automation"
    assert result["confidence"] > 0
    assert result["confidence"] <= 0.95
    assert len(result["reasoning"]) > 0

def test_context_classifier_reporting():
    prompt = "generate a report and a dashboard with key metrics"
    result = ContextClassifier.classify(prompt)
    assert result["context"] == "Reporting and Analytics"

def test_context_classifier_fallback():
    prompt = "hello world"
    result = ContextClassifier.classify(prompt)
    assert result["context"] == FALLBACK_CONTEXT
    assert result["confidence"] == 1.0

def test_diagnosis_engine_strong():
    prompt = "Create a report for the manager. Output format should be JSON. Ensure it meets the success KPI. Exception handling is fallback to defaults. Must be under budget. Criteria for decision is cost."
    result = DiagnosisEngine.diagnose(prompt)
    assert result["strength"] == "Strong"
    assert len(result["missing_elements"]) == 0
    assert len(result["execution_risks"]) == 0

def test_diagnosis_engine_broken():
    prompt = "just do something"
    result = DiagnosisEngine.diagnose(prompt)
    assert result["strength"] == "Broken"
    assert "no objective" in result["missing_elements"]
    assert "no audience" in result["missing_elements"]
    assert "no output format" in result["missing_elements"]
    assert "Lack of Clear Purpose" in result["execution_risks"]
    assert "Misaligned Recommendations" in result["execution_risks"]
    assert "Ambiguous Output" in result["execution_risks"]

def test_diagnosis_engine_partial():
    # Only objective and audience
    prompt = "Build a solution for the executive"
    result = DiagnosisEngine.diagnose(prompt)
    assert result["strength"] == "Broken"
    assert "no output format" in result["missing_elements"]

def test_context_classifier_confidence_calculation():
    # Process Automation: 'workflow', 'automation', 'trigger' (3 matches)
    # Workflow Design: 'trigger' (1 match, workflow doesn't match 'workflow design')
    # Total = 4 matches. 3 / 4 = 0.75
    prompt = "A workflow for automation with a trigger"
    result = ContextClassifier.classify(prompt)
    assert result["context"] == "Process Automation"
    assert result["confidence"] == 0.75
