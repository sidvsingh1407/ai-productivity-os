import pytest
import json
from unittest.mock import patch, AsyncMock
from services.narrative_service import generate_audit_narrative, _parse_gemini_json

VALID_JSON = """{
  "executive_summary": {
    "overall_assessment": "This is a valid assessment.",
    "critical_risk": "Data exposure.",
    "primary_opportunity": "Automation.",
    "recommended_first_action": "Audit access."
  },
  "dimension_narratives": {
    "awareness": "Good awareness.",
    "adoption": "High adoption.",
    "integration": "Poor integration.",
    "governance": "Lacking governance.",
    "roi": "Low ROI."
  }
}"""

INVALID_JSON = """{
  "executive_summary": {
"""

MISSING_FIELDS_JSON = """{
  "executive_summary": {
    "overall_assessment": "Valid assessment."
  },
  "dimension_narratives": {
    "awareness": "Good awareness."
  }
}"""

LONG_STRING_JSON = json.dumps({
    "executive_summary": {
        "overall_assessment": "A" * 1500, # Too long
        "critical_risk": "Data exposure.",
        "primary_opportunity": "Automation.",
        "recommended_first_action": "Audit access."
    },
    "dimension_narratives": {
        "awareness": "Good awareness.",
        "adoption": "High adoption.",
        "integration": "Poor integration.",
        "governance": "Lacking governance.",
        "roi": "Low ROI."
    }
})

@pytest.mark.asyncio
async def test_generate_audit_narrative_valid():
    with patch('services.gemini_client.gemini_manager.generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = VALID_JSON
        scores = {}
        context = {}
        result = await generate_audit_narrative(scores, context)

        assert result is not None
        assert "executive_summary" in result
        assert "dimension_narratives" in result
        assert result["executive_summary"]["overall_assessment"] == "This is a valid assessment."

@pytest.mark.asyncio
async def test_generate_audit_narrative_invalid_json():
    with patch('services.gemini_client.gemini_manager.generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = INVALID_JSON
        scores = {}
        context = {}
        result = await generate_audit_narrative(scores, context)

        assert result is None

@pytest.mark.asyncio
async def test_generate_audit_narrative_missing_fields():
    with patch('services.gemini_client.gemini_manager.generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = MISSING_FIELDS_JSON
        scores = {}
        context = {}
        result = await generate_audit_narrative(scores, context)

        assert result is None

@pytest.mark.asyncio
async def test_generate_audit_narrative_long_string():
    with patch('services.gemini_client.gemini_manager.generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = LONG_STRING_JSON
        scores = {}
        context = {}
        result = await generate_audit_narrative(scores, context)

        assert result is None

@pytest.mark.asyncio
async def test_generate_audit_narrative_gemini_fails():
    with patch('services.gemini_client.gemini_manager.generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = None
        scores = {}
        context = {}
        result = await generate_audit_narrative(scores, context)

        assert result is None

def test_parse_gemini_json():
    raw = "```json\n" + VALID_JSON + "\n```"
    result = _parse_gemini_json(raw)
    assert result is not None
    assert result["executive_summary"]["overall_assessment"] == "This is a valid assessment."
