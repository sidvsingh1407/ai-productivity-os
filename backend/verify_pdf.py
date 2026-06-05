import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from reports.pdf_generator import generate_audit_pdf

with open('offline_sample_payload.json', 'r') as f:
    payload = json.load(f)

# The payload root has "scores" which is already the dimensions object
# Let's fix it up for the PDF generator
payload["scores"] = {"dimensions": payload["scores"]}

generate_audit_pdf(payload, 'sample_output.pdf')
print("Sample PDF generated at sample_output.pdf")
