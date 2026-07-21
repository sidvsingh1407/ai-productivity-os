import os
import pypdf
import pytest
from reports.pdf_generator import generate_audit_pdf

# Note: There were no prior tests verifying the content/structure of the generated PDF in this repository.
# These tests explicitly verify that the Per-System Findings section is correctly populated or omitted based on the input.

@pytest.fixture
def sample_audit_data_with_systems():
    return {
        "company_name": "Test Company",
        "scores": {},
        "intelligence": {
            "executive_summary": {"overall_assessment": "Test Exec Summary"},
            "findings": [
                {
                    "severity": "High",
                    "title": "Flat Finding Title",
                    "impact": "Flat Finding Impact",
                    "rationale": "Flat Finding Rationale"
                }
            ],
            "recommendations": [
                {
                    "priority": "High",
                    "recommendation": "Flat Recommendation",
                    "expected_impact": "High Impact",
                    "effort": "Low"
                }
            ],
            "roadmap": {}
        },
        "system_findings": [
            {
                "ai_system_id": "sys-1",
                "ai_system_name": "Alpha System",
                "findings": [
                    {
                        "severity": "Critical",
                        "title": "Alpha Finding Title",
                        "impact": "Alpha Finding Impact",
                        "rationale": "Alpha Finding Rationale"
                    }
                ],
                "recommendations": [
                    {
                        "priority": "Critical",
                        "recommendation": "Alpha Recommendation",
                        "expected_impact": "Critical Impact",
                        "effort": "High"
                    }
                ]
            },
            {
                "ai_system_id": "sys-2",
                "ai_system_name": "Beta System",
                "findings": [],
                "recommendations": []
            }
        ]
    }

@pytest.fixture
def sample_audit_data_without_systems():
    return {
        "company_name": "Test Company",
        "scores": {},
        "intelligence": {
            "executive_summary": {"overall_assessment": "Test Exec Summary"},
            "findings": [],
            "recommendations": [],
            "roadmap": {}
        }
    }


def _extract_pdf_text(filepath):
    text = ""
    with open(filepath, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def test_generate_audit_pdf_with_system_findings(tmp_path, sample_audit_data_with_systems):
    output_path = tmp_path / "test_with_systems.pdf"
    result_path = generate_audit_pdf(sample_audit_data_with_systems, str(output_path))

    assert os.path.exists(result_path)

    text = _extract_pdf_text(result_path)

    # Assert standard components are present
    assert "Test Company" in text
    assert "Flat Finding Title" in text

    # Assert Per-System section is present
    assert "Per-System Findings" in text

    # Assert Alpha System details
    assert "Alpha System" in text
    assert "Alpha Finding Title" in text
    assert "Alpha Recommendation" in text

    # Assert Beta System details (empty findings/recs)
    assert "Beta System" in text
    assert "No findings." in text
    assert "No specific recommendations provided." in text

def test_generate_audit_pdf_without_system_findings(tmp_path, sample_audit_data_without_systems):
    output_path = tmp_path / "test_without_systems.pdf"
    result_path = generate_audit_pdf(sample_audit_data_without_systems, str(output_path))

    assert os.path.exists(result_path)

    text = _extract_pdf_text(result_path)

    # Assert standard components are present
    assert "Test Company" in text

    # Assert Per-System section is NOT present
    assert "Per-System Findings" not in text
    assert "Alpha System" not in text
