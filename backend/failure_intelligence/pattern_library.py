"""
Failure Pattern Library for TarkaX.
Defines the 10 core failure patterns, their deterministic triggers, root causes, consequences, and interventions.
"""
from typing import Dict, Any, List

FAILURE_PATTERNS = [
    {
        "id": "fp_governance_vacuum",
        "name": "Governance Vacuum",
        "description": "Lack of centralized oversight, policies, or dedicated ownership for AI initiatives, leading to unmanaged risk.",
        "trigger_conditions": {
            "governance_score_threshold": 40, # Out of 100
        },
        "severity": "Critical",
        "root_causes": [
            "No formal governance ownership",
            "Undefined AI policies and guidelines",
            "Decentralized and unmonitored adoption"
        ],
        "consequences": [
            "Severe compliance risk and legal exposure",
            "Inconsistent AI usage leading to quality issues",
            "Duplicated tooling and shadow IT"
        ],
        "interventions": [
            {
                "intervention": "Establish an AI Governance Committee",
                "impact": "High",
                "effort": "Medium"
            },
            {
                "intervention": "Draft and enforce an Acceptable AI Use Policy",
                "impact": "High",
                "effort": "Low"
            }
        ]
    },
    {
        "id": "fp_ai_experimentation_without_ownership",
        "name": "AI Experimentation Without Ownership",
        "description": "AI initiatives are being tested or deployed in silos without clear business ownership or strategic alignment.",
        "trigger_conditions": {
            "awareness_score_high": 60, # High awareness
            "adoption_score_low": 40,   # But low formal adoption
        },
        "severity": "Major",
        "root_causes": [
            "Lack of designated business sponsors for AI projects",
            "Innovation happening bottom-up without top-down alignment",
            "Unclear pathways from POC to production"
        ],
        "consequences": [
            "Abandoned projects after initial hype",
            "Wasted resources on unscalable experiments",
            "Frustration among early adopters"
        ],
        "interventions": [
            {
                "intervention": "Mandate business sponsors for all active AI pilots",
                "impact": "High",
                "effort": "Medium"
            }
        ]
    },
    {
        "id": "fp_tool_proliferation",
        "name": "Tool Proliferation",
        "description": "Explosion of disparate AI tools across departments, creating a fragmented technology landscape.",
        "trigger_conditions": {
            "integration_score_low": 40,
            "adoption_score_moderate": 40, # At least moderate adoption
        },
        "severity": "Major",
        "root_causes": [
            "Individual departments purchasing tools independently",
            "Lack of centralized IT procurement for AI",
            "No standardized technology stack"
        ],
        "consequences": [
            "Unnecessary software spend and licensing bloat",
            "Fragmented workflows and data silos",
            "Adoption fatigue as employees juggle multiple tools"
        ],
        "interventions": [
            {
                "intervention": "Conduct an immediate AI vendor rationalization audit",
                "impact": "High",
                "effort": "Medium"
            },
            {
                "intervention": "Establish centralized IT procurement policies for AI tools",
                "impact": "High",
                "effort": "Medium"
            }
        ]
    },
    {
        "id": "fp_shadow_ai_adoption",
        "name": "Shadow AI Adoption",
        "description": "Employees are using unapproved, potentially insecure AI tools (e.g., consumer LLMs) for company work.",
        "trigger_conditions": {
            "governance_score_low": 50,
            "adoption_score_high": 60,
        },
        "severity": "Critical",
        "root_causes": [
            "Company-provided tools do not meet employee needs",
            "Lack of awareness regarding data privacy risks",
            "Absence of technical controls blocking unauthorized tools"
        ],
        "consequences": [
            "Data breaches and intellectual property leakage",
            "Loss of control over company data and workflows",
            "Unquantifiable compliance exposure"
        ],
        "interventions": [
            {
                "intervention": "Deploy secure, enterprise-approved AI alternatives immediately",
                "impact": "High",
                "effort": "High"
            },
            {
                "intervention": "Implement technical controls to monitor and block unauthorized AI platforms",
                "impact": "High",
                "effort": "Medium"
            }
        ]
    },
    {
        "id": "fp_no_roi_measurement",
        "name": "No ROI Measurement",
        "description": "Inability to track, measure, or quantify the business value and impact of AI investments.",
        "trigger_conditions": {
            "roi_score_low": 40,
        },
        "severity": "Moderate",
        "root_causes": [
            "Failure to define success metrics before deploying tools",
            "Lack of baseline performance data for comparison",
            "Disconnect between AI usage and business objectives"
        ],
        "consequences": [
            "Inability to justify ongoing or future AI investments",
            "Risk of leadership losing faith in AI programs",
            "Misallocation of budget to low-impact tools"
        ],
        "interventions": [
            {
                "intervention": "Define standard KPIs (time saved, cost reduced) for all AI use cases",
                "impact": "High",
                "effort": "Medium"
            },
            {
                "intervention": "Implement baseline tracking before any new AI rollout",
                "impact": "Medium",
                "effort": "Medium"
            }
        ]
    },
    {
        "id": "fp_fragmented_ai_strategy",
        "name": "Fragmented AI Strategy",
        "description": "Different parts of the organization have conflicting goals and uncoordinated approaches to AI.",
        "trigger_conditions": {
            "contradictions_exist": True,
        },
        "severity": "Major",
        "root_causes": [
            "Lack of a unified, enterprise-level AI vision",
            "Siloed departmental planning and budgeting",
            "Poor communication between IT and business units"
        ],
        "consequences": [
            "Misaligned investments and duplicated effort",
            "Internal friction and political bottlenecks",
            "Inability to scale successful AI pilots enterprise-wide"
        ],
        "interventions": [
            {
                "intervention": "Develop and communicate a unified Enterprise AI Vision",
                "impact": "High",
                "effort": "High"
            },
            {
                "intervention": "Create cross-functional AI working groups to align initiatives",
                "impact": "Medium",
                "effort": "Medium"
            }
        ]
    },
    {
        "id": "fp_executive_misalignment",
        "name": "Executive Misalignment",
        "description": "Leadership lacks consensus on AI priorities, risks, or required investment levels.",
        "trigger_conditions": {
            "awareness_score_low": 40,
            "governance_score_low": 50,
        },
        "severity": "Major",
        "root_causes": [
            "Varying levels of AI literacy among the executive team",
            "Conflicting priorities between innovation and risk management",
            "Lack of clear business cases presented to leadership"
        ],
        "consequences": [
            "Stalled decision-making and delayed funding",
            "Mixed messages sent to the broader organization",
            "Failure to capitalize on strategic AI opportunities"
        ],
        "interventions": [
            {
                "intervention": "Conduct an executive AI briefing and alignment workshop",
                "impact": "High",
                "effort": "Low"
            }
        ]
    },
    {
        "id": "fp_low_workforce_readiness",
        "name": "Low Workforce Readiness",
        "description": "The general workforce lacks the necessary skills, training, or motivation to adopt AI tools effectively.",
        "trigger_conditions": {
            "awareness_score_low": 50,
            "adoption_score_low": 40,
        },
        "severity": "Moderate",
        "root_causes": [
            "Inadequate training programs or resources",
            "Fear of job displacement or change resistance",
            "Complex tools deployed without proper change management"
        ],
        "consequences": [
            "Low adoption rates for deployed AI tools",
            "Missed productivity gains and efficiency improvements",
            "Increased error rates as employees misuse tools"
        ],
        "interventions": [
            {
                "intervention": "Launch a comprehensive, role-based AI literacy program",
                "impact": "High",
                "effort": "High"
            },
            {
                "intervention": "Identify and empower departmental 'AI Champions' to drive peer adoption",
                "impact": "Medium",
                "effort": "Medium"
            }
        ]
    },
    {
        "id": "fp_poor_workflow_integration",
        "name": "Poor Workflow Integration",
        "description": "AI tools are treated as standalone applications rather than integrated into core business processes.",
        "trigger_conditions": {
            "integration_score_low": 30,
        },
        "severity": "Major",
        "root_causes": [
            "Legacy systems incompatible with modern AI APIs",
            "Failure to map end-to-end business processes before deployment",
            "Over-reliance on 'copy-paste' manual AI workflows"
        ],
        "consequences": [
            "Creation of new process bottlenecks",
            "Data inconsistencies across disjointed systems",
            "Failure to achieve scalable, automated efficiencies"
        ],
        "interventions": [
            {
                "intervention": "Map core business processes to identify explicit AI integration points",
                "impact": "High",
                "effort": "Medium"
            },
            {
                "intervention": "Invest in API development or middleware to connect AI tools with legacy systems",
                "impact": "High",
                "effort": "High"
            }
        ]
    },
    {
        "id": "fp_compliance_exposure",
        "name": "Compliance Exposure",
        "description": "Immediate regulatory, legal, or data privacy risks stemming from current AI usage.",
        "trigger_conditions": {
            "compliance_risk_flag": True,
        },
        "severity": "Critical",
        "root_causes": [
            "Handling sensitive data (PII, PHI) in public or non-compliant LLMs",
            "Lack of legal review for AI vendor contracts",
            "Ignorance of industry-specific AI regulations"
        ],
        "consequences": [
            "Regulatory fines and legal penalties",
            "Loss of customer trust and brand damage",
            "Forced cessation of critical business operations"
        ],
        "interventions": [
            {
                "intervention": "Immediately halt usage of non-compliant AI tools for sensitive data",
                "impact": "High",
                "effort": "Low"
            },
            {
                "intervention": "Conduct a formal legal and security review of all active AI vendors",
                "impact": "High",
                "effort": "Medium"
            }
        ]
    }
]
