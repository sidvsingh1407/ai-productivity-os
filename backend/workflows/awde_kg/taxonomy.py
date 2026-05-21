from __future__ import annotations


PROCESS_NODES = [
    {
        "process_id": "process:finance:vendor_invoice_matching",
        "node_type": "process",
        "title": "Vendor invoice matching",
        "apqc_reference": {"category": "Finance", "id": "apqc-ref-finance-payables"},
        "industry_variants": [
            {
                "industry_tag": "healthcare",
                "delta_tools": ["capability:decision_support"],
                "delta_hitl_weight": 0.25,
                "compliance_flags": ["HIPAA", "PHI"],
                "confidence": 0.78,
            },
            {
                "industry_tag": "banking",
                "delta_tools": ["capability:orchestration"],
                "delta_hitl_weight": 0.2,
                "compliance_flags": ["SOX", "AML"],
                "confidence": 0.76,
            },
        ],
    },
    {
        "process_id": "process:hr:employee_service_intake",
        "node_type": "process",
        "title": "Employee service intake",
        "apqc_reference": {"category": "Human Capital Management", "id": "apqc-ref-hr-service"},
        "industry_variants": [],
    },
    {
        "process_id": "process:procurement:vendor_onboarding",
        "node_type": "process",
        "title": "Vendor onboarding",
        "apqc_reference": {"category": "Procurement", "id": "apqc-ref-procurement-vendor"},
        "industry_variants": [
            {
                "industry_tag": "public_sector",
                "delta_tools": ["capability:decision_support"],
                "delta_hitl_weight": 0.3,
                "compliance_flags": ["procurement_policy", "audit_retention"],
                "confidence": 0.72,
            }
        ],
    },
    {
        "process_id": "process:customer_support:ticket_triage",
        "node_type": "process",
        "title": "Customer support ticket triage",
        "apqc_reference": {"category": "Customer Service", "id": "apqc-ref-customer-service"},
        "industry_variants": [],
    },
    {
        "process_id": "process:it:incident_response",
        "node_type": "process",
        "title": "IT incident response",
        "apqc_reference": {"category": "Information Technology", "id": "apqc-ref-it-incident"},
        "industry_variants": [
            {
                "industry_tag": "regulated_enterprise",
                "delta_tools": ["capability:decision_support"],
                "delta_hitl_weight": 0.25,
                "compliance_flags": ["SOC2", "ISO27001"],
                "confidence": 0.75,
            }
        ],
    },
    {
        "process_id": "process:legal:contract_review",
        "node_type": "process",
        "title": "Contract review intake",
        "apqc_reference": {"category": "Legal", "id": "apqc-ref-legal-contract"},
        "industry_variants": [],
    },
    {
        "process_id": "process:legal:contract_review_and_redlining",
        "node_type": "process",
        "title": "Contract Review and Redlining",
        "apqc_reference": {"category": "Legal", "id": "apqc-ref-legal-contract-redlining"},
        "industry_variants": [
            {
                "industry_tag": "regulated_enterprise",
                "delta_tools": ["capability:decision_support", "capability:audit_trail"],
                "delta_hitl_weight": 0.3,
                "compliance_flags": ["contract_playbook", "approval_authority", "audit_retention"],
                "confidence": 0.78,
            }
        ],
    },
    {
        "process_id": "process:ops:customer_support_ticket_triage",
        "node_type": "process",
        "title": "Customer Support Ticket Triage",
        "apqc_reference": {"category": "Operations", "id": "apqc-ref-ops-customer-ticket-triage"},
        "industry_variants": [
            {
                "industry_tag": "saas",
                "delta_tools": ["capability:classification", "capability:orchestration"],
                "delta_hitl_weight": 0.15,
                "compliance_flags": ["sla_policy", "customer_data_handling"],
                "confidence": 0.8,
            }
        ],
    },
    {
        "process_id": "process:healthcare:patient_intake_form_processing",
        "node_type": "process",
        "title": "Patient Intake Form Processing",
        "apqc_reference": {"category": "Healthcare Operations", "id": "apqc-ref-healthcare-patient-intake"},
        "industry_variants": [
            {
                "industry_tag": "healthcare",
                "delta_tools": ["capability:document_extraction", "capability:decision_support"],
                "delta_hitl_weight": 0.35,
                "compliance_flags": ["HIPAA", "PHI", "consent_validation"],
                "confidence": 0.82,
            }
        ],
    },
    {
        "process_id": "process:procurement:rfp_response_extraction",
        "node_type": "process",
        "title": "RFP Response Extraction",
        "apqc_reference": {"category": "Procurement", "id": "apqc-ref-procurement-rfp-response"},
        "industry_variants": [
            {
                "industry_tag": "public_sector",
                "delta_tools": ["capability:document_extraction", "capability:policy_compliance"],
                "delta_hitl_weight": 0.28,
                "compliance_flags": ["bid_policy", "vendor_disclosure", "audit_retention"],
                "confidence": 0.76,
            }
        ],
    },
    {
        "process_id": "process:hr:employee_offboarding_checklist",
        "node_type": "process",
        "title": "Employee Offboarding Checklist",
        "apqc_reference": {"category": "Human Capital Management", "id": "apqc-ref-hr-offboarding-checklist"},
        "industry_variants": [
            {
                "industry_tag": "regulated_enterprise",
                "delta_tools": ["capability:orchestration", "capability:security_review"],
                "delta_hitl_weight": 0.22,
                "compliance_flags": ["access_revocation", "asset_return", "policy_acknowledgement"],
                "confidence": 0.77,
            }
        ],
    },
    {
        "process_id": "process:finance:accounts_receivable_dunning",
        "node_type": "process",
        "title": "Accounts Receivable Dunning",
        "apqc_reference": {"category": "Finance", "id": "apqc-ref-finance-ar-dunning"},
        "industry_variants": [
            {
                "industry_tag": "banking",
                "delta_tools": ["capability:classification", "capability:audit_trail"],
                "delta_hitl_weight": 0.2,
                "compliance_flags": ["collections_policy", "customer_communication", "audit_retention"],
                "confidence": 0.75,
            }
        ],
    },
]

FRICTION_PATTERN_NODES = [
    {
        "friction_id": "friction:cognitive:document_cross_reference",
        "node_type": "friction_pattern",
        "friction_type": "cognitive",
        "title": "Document cross-reference burden",
        "signals": ["pdf", "policy", "manual review", "cross-reference"],
        "confidence": 0.86,
    },
    {
        "friction_id": "friction:mechanical:system_rekeying",
        "node_type": "friction_pattern",
        "friction_type": "mechanical",
        "title": "Manual system rekeying",
        "signals": ["copy paste", "erp", "crm", "screens"],
        "confidence": 0.84,
    },
    {
        "friction_id": "friction:cognitive:triage_and_routing",
        "node_type": "friction_pattern",
        "friction_type": "cognitive",
        "title": "Triage and routing ambiguity",
        "signals": ["ticket", "queue", "priority", "routing"],
        "confidence": 0.82,
    },
    {
        "friction_id": "friction:mechanical:approval_followup",
        "node_type": "friction_pattern",
        "friction_type": "mechanical",
        "title": "Approval follow-up work",
        "signals": ["approval", "slack", "email", "reminder"],
        "confidence": 0.81,
    },
]

CAPABILITY_NODES = [
    {
        "capability_id": "capability:document_extraction",
        "node_type": "capability",
        "title": "Document extraction",
        "capability_type": "document_extraction",
        "tools": ["Claude", "Gemini", "OpenAI"],
        "confidence": 0.86,
    },
    {
        "capability_id": "capability:decision_support",
        "node_type": "capability",
        "title": "Decision support",
        "capability_type": "decision_support",
        "tools": ["Claude", "Gemini", "OpenAI"],
        "confidence": 0.84,
    },
    {
        "capability_id": "capability:orchestration",
        "node_type": "capability",
        "title": "No-code workflow orchestration",
        "capability_type": "orchestration",
        "tools": ["n8n", "Zapier", "Make"],
        "confidence": 0.88,
    },
    {
        "capability_id": "capability:classification",
        "node_type": "capability",
        "title": "Classification",
        "capability_type": "classification",
        "tools": ["Claude", "Gemini", "OpenAI"],
        "confidence": 0.85,
    },
    {
        "capability_id": "capability:summarization",
        "node_type": "capability",
        "title": "Summarization",
        "capability_type": "summarization",
        "tools": ["Claude", "Gemini", "OpenAI"],
        "confidence": 0.82,
    },
    {
        "capability_id": "capability:entity_resolution",
        "node_type": "capability",
        "title": "Entity resolution",
        "capability_type": "entity_resolution",
        "tools": ["Claude", "Gemini", "OpenAI", "rules engine"],
        "confidence": 0.83,
    },
    {
        "capability_id": "capability:human_approval",
        "node_type": "capability",
        "title": "Human approval checkpoint",
        "capability_type": "hitl",
        "tools": ["Slack", "Teams", "ServiceNow"],
        "confidence": 0.87,
    },
    {
        "capability_id": "capability:system_writeback",
        "node_type": "capability",
        "title": "System writeback",
        "capability_type": "execution",
        "tools": ["SAP", "Salesforce", "Workday", "RPA"],
        "confidence": 0.8,
    },
    {
        "capability_id": "capability:compliance_review",
        "node_type": "capability",
        "title": "Compliance review",
        "capability_type": "governance",
        "tools": ["policy engine", "audit log"],
        "confidence": 0.78,
    },
    {
        "capability_id": "capability:audit_trail",
        "node_type": "capability",
        "title": "Audit trail capture",
        "capability_type": "governance",
        "tools": ["database", "event log"],
        "confidence": 0.79,
    },
    {
        "capability_id": "capability:policy_compliance",
        "node_type": "capability",
        "title": "Policy compliance check",
        "capability_type": "governance",
        "tools": ["rules engine", "document store"],
        "confidence": 0.76,
    },
    {
        "capability_id": "capability:security_review",
        "node_type": "capability",
        "title": "Security review",
        "capability_type": "governance",
        "tools": ["SIEM", "ticketing"],
        "confidence": 0.76,
    },
]
