from typing import Dict, Any

INDUSTRY_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "HEALTHCARE": {
        "challenges": [
            "Strict patient data privacy regulations (HIPAA, GDPR)",
            "Clinical validation of AI models",
            "Integration with legacy EHR systems"
        ],
        "risks": [
            "Patient Safety Risk: AI providing incorrect clinical decision support.",
            "Compliance Risk: Mishandling PHI in cloud-based AI tools."
        ],
        "best_practices": [
            "Implement a formal clinical AI governance board.",
            "Require explicit consent frameworks for data usage."
        ],
        "failure_patterns": [
            "Adopting clinical AI without sufficient data de-identification protocols.",
            "Deploying AI chatbots for triage without human oversight."
        ],
        "governance_finding": {
            "title": "Patient Data Governance Risk",
            "impact": "Exposure to HIPAA violations and patient privacy breaches.",
            "rationale": "AI governance structure lacks specific controls for clinical and patient data."
        },
        "governance_recommendation": {
            "recommendation": "Establish clinical data governance controls specific to AI usage.",
            "expected_impact": "High",
            "implementation_effort": "High"
        }
    },
    "SAAS": {
        "challenges": [
            "Rapid product iteration outpaces AI governance",
            "Integrating AI features natively into user workflows",
            "Measuring true ROI of AI features vs core product"
        ],
        "risks": [
            "AI Product Governance Risk: Unregulated AI features reaching production.",
            "Adoption Risk: Users ignoring AI features due to poor UX."
        ],
        "best_practices": [
            "Embed AI governance directly into the SDLC.",
            "Measure AI feature adoption with dedicated product analytics."
        ],
        "failure_patterns": [
            "Shipping 'wrapper' features without core product differentiation.",
            "Overestimating user readiness for autonomous agents."
        ],
        "governance_finding": {
            "title": "AI Product Governance Risk",
            "impact": "Deploying unregulated AI features that hallucinate or leak tenant data.",
            "rationale": "Product development lacks a formal AI feature approval and testing process."
        },
        "governance_recommendation": {
            "recommendation": "Integrate AI security and quality gates into the standard SDLC.",
            "expected_impact": "High",
            "implementation_effort": "Medium"
        }
    },
    "GOVERNMENT": {
        "challenges": [
            "Public procurement cycles delay AI adoption",
            "High requirement for transparency and explainability",
            "Citizen trust and accountability"
        ],
        "risks": [
            "Public-Sector Accountability Risk: Inability to explain AI-driven civic decisions.",
            "Procurement Risk: Getting locked into rigid, legacy AI contracts."
        ],
        "best_practices": [
            "Develop responsible AI frameworks aligned with public policy.",
            "Require vendor algorithmic transparency."
        ],
        "failure_patterns": [
            "Deploying black-box AI for public service eligibility.",
            "Failing to conduct public impact assessments before deployment."
        ],
        "governance_finding": {
            "title": "Public-Sector AI Accountability Risk",
            "impact": "Erosion of public trust and potential civil rights violations.",
            "rationale": "Governance lacks transparency requirements for citizen-facing AI."
        },
        "governance_recommendation": {
            "recommendation": "Implement a public-sector Responsible AI framework with mandatory impact assessments.",
            "expected_impact": "High",
            "implementation_effort": "High"
        }
    },
    "MANUFACTURING": {
        "challenges": [
            "IT/OT convergence and legacy equipment",
            "Data silos between factory floor and enterprise systems",
            "Workforce resistance on the shop floor"
        ],
        "risks": [
            "Operational Technology (OT) Risk: AI models causing production line downtime.",
            "Safety Risk: Unpredictable AI behavior in physical environments."
        ],
        "best_practices": [
            "Deploy AI at the edge for real-time latency requirements.",
            "Focus initially on predictive maintenance rather than autonomous control."
        ],
        "failure_patterns": [
            "Attempting factory-wide AI before establishing a unified data historian.",
            "Ignoring shop-floor operator input during AI model training."
        ],
        "integration_finding": {
            "title": "IT/OT AI Integration Bottleneck",
            "impact": "Inability to deploy AI to the factory floor, limiting ROI.",
            "rationale": "Disconnect between enterprise data systems and operational technology."
        },
        "integration_recommendation": {
            "recommendation": "Bridge IT/OT data silos to enable edge AI deployments.",
            "expected_impact": "High",
            "implementation_effort": "High"
        }
    },
    "BANKING": {
        "challenges": [
            "Heavy regulatory scrutiny (e.g., algorithmic bias)",
            "Legacy core banking systems",
            "High stakes of model drift in financial decisions"
        ],
        "risks": [
            "Regulatory Model Risk: Non-compliance with financial AI regulations.",
            "Systemic Risk: AI models making cascading poor financial decisions."
        ],
        "best_practices": [
            "Implement Model Risk Management (MRM) frameworks for all AI.",
            "Maintain strict separation of training and production environments."
        ],
        "failure_patterns": [
            "Using generative AI for direct financial advice without HITL.",
            "Failing to document model lineage for regulatory audits."
        ],
        "governance_finding": {
            "title": "Algorithmic Model Risk Management",
            "impact": "Regulatory fines and biased financial decision-making.",
            "rationale": "AI governance is not integrated with existing Model Risk Management (MRM)."
        },
        "governance_recommendation": {
            "recommendation": "Expand existing Model Risk Management frameworks to explicitly cover Generative AI.",
            "expected_impact": "High",
            "implementation_effort": "Medium"
        }
    }
}
