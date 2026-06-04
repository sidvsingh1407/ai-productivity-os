import json
import os
import sys

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reports.pdf_generator import generate_audit_pdf
from audits.intelligence_engine import generate_intelligence

# Create a sample payload for PDF generation
scores_dict = {
    'dimensions': {
        'awareness': 10,
        'adoption': 12,
        'integration': 5,
        'governance': 8,
        'roi': 6
    },
    'compliance_risk_flag': True,
    'compliance_risk_reasons': ['No EU AI Act mapping', 'Usage of unapproved models'],
    'contradictions': [
        {'type': 'contradiction', 'title': 'Policy vs Practice', 'description': 'Policy exists but no enforcement.'}
    ],
    'missing_data_flags': []
}

total_score = sum(scores_dict['dimensions'].values())

intelligence = generate_intelligence(scores_dict)

audit_data = {
    "company_name": "TarkaX Verify Org",
    "scores": scores_dict,
    "total_score": total_score,
    "rating": "Developing",
    "compliance_risk_flag": True,
    "compliance_risk_reasons": ['No EU AI Act mapping', 'Usage of unapproved models'],
    "intelligence": intelligence
}

# Dump sample payload for verification evidence
with open("sample_payload.json", "w") as f:
    json.dump(audit_data, f, indent=2)

# Generate PDF
output_pdf_path = "sample_output.pdf"
generate_audit_pdf(audit_data, output_pdf_path)

print(f"Sample PDF generated at {output_pdf_path}")
print(f"Sample Payload generated at sample_payload.json")
