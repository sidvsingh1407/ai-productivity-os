# TarkaX B1 — API Readiness & Contract Design Audit

## Executive Summary

This document outlines the API readiness of TarkaX’s core intelligence capabilities. The objective is to define stable API contracts and identify the minimum refactoring required to make TarkaX consumable as a third-party API product.

Currently, only the **Prompt Improver** is fully designed as a stateless, API-ready service. Stateful products like **AI Audit** and **Workflow Diagnostic** require authentication context refactoring (API keys vs. JWTs) to decouple them from the UI. Internal engines like **Risk Projection** and **Failure Intelligence** require the creation of dedicated service and routing layers to be exposed independently.

## Capability Matrix

| Product | API Ready | Refactor Needed | Notes |
| :--- | :--- | :--- | :--- |
| **Prompt Improver** | API Ready | None | Fully stateless, dedicated schemas and service layer exist. Can be exposed immediately. |
| **AI Audit** | Requires Refactoring | Minor | Requires refactoring to abstract `user_id` and `org_id` resolution from an API key. Currently tied to internal auth dependencies. |
| **Workflow Diagnostic** | Requires Refactoring | Minor | Requires refactoring for API key auth context mapping. Relies on internal pipeline execution. |
| **Risk Projection** | Not Ready | Major | Currently an internal engine function. Lacks dedicated request/response schemas and a standalone API route. |
| **Failure Intelligence** | Not Ready | Major | Currently an internal engine function. Lacks dedicated request/response schemas and a standalone API route. |

---

## Proposed Endpoints

* `POST /api/v1/prompt-improver`
* `POST /api/v1/audit`
* `POST /api/v1/workflow`
* `POST /api/v1/risk`
* `POST /api/v1/failure-intelligence`

---

## Request Schemas

### POST /api/v1/prompt-improver
* **Required Fields:** `prompt` (string)
* **Optional Fields:** None
* **Validation Rules:** `prompt` must not be empty. Maximum length is 10,000 characters.
* **Maximum Payload Size:** 50 KB

**Example Request:**
```json
{
  "prompt": "Write me an email to the team about our new AI policy."
}
```

### POST /api/v1/audit
* **Required Fields:** `form_response` (object)
* **Optional Fields:** `evidence_response` (object), `industry_type` (string)
* **Validation Rules:** `form_response` must contain valid assessment keys corresponding to the scoring engine.
* **Maximum Payload Size:** 250 KB

**Example Request:**
```json
{
  "form_response": {
    "question_1": "yes",
    "question_2": "partial"
  },
  "industry_type": "technology"
}
```

### POST /api/v1/workflow
* **Required Fields:** `input_config` (object)
* **Optional Fields:** None
* **Validation Rules:** Must contain the required configuration keys to execute the workflow intelligence pipeline.
* **Maximum Payload Size:** 500 KB

**Example Request:**
```json
{
  "input_config": {
    "workflow_name": "Invoice Processing",
    "steps": 15,
    "manual_handoffs": 4
  }
}
```

### POST /api/v1/risk
* **Required Fields:** `dimension_scores` (object)
* **Optional Fields:** `missing_data` (array of strings)
* **Validation Rules:** `dimension_scores` must contain numeric scores.
* **Maximum Payload Size:** 100 KB

**Example Request:**
```json
{
  "dimension_scores": {
    "governance": 60,
    "adoption": 80,
    "integration": 50,
    "roi": 40
  },
  "missing_data": ["financials"]
}
```

### POST /api/v1/failure-intelligence
* **Required Fields:** `scores` (object)
* **Optional Fields:** `compliance_risk_flag` (boolean), `contradictions` (array)
* **Validation Rules:** `scores` must map to valid dimension keys.
* **Maximum Payload Size:** 100 KB

**Example Request:**
```json
{
  "scores": {
    "dimensions": {
      "governance": 12,
      "adoption": 15
    }
  },
  "compliance_risk_flag": true,
  "contradictions": []
}
```

---

## Response Contracts

### POST /api/v1/prompt-improver
**Success Response:**
```json
{
  "context": {
    "category": "Communication",
    "confidence": 0.95
  },
  "diagnosis": {
    "strength": "Weak",
    "missing": ["Context", "Tone"],
    "execution_risks": ["Ambiguity"]
  },
  "scores": {
    "original_score": 40,
    "improved_score": 85
  },
  "validation": {
    "passed": true,
    "errors": []
  },
  "improved_prompt": "Act as a department head. Write an email to the team announcing our new AI policy. Keep the tone professional but encouraging.",
  "rationale": {
    "changes_made": ["Added structural elements: Context, Tone", "Optimized instructions for clarity and objective focus."],
    "failure_modes_addressed": ["Ambiguity"]
  }
}
```

**Error Response:**
```json
{
  "detail": "Prompt cannot be empty"
}
```

### POST /api/v1/audit
**Success Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "complete",
  "total_score": 75,
  "intelligence": {
    "executive_summary": {
      "overall_assessment": "The organization shows strong adoption but lacks governance.",
      "critical_risk": "High risk of shadow IT.",
      "primary_opportunity": "Centralize AI procurement.",
      "recommended_first_action": "Establish AI Governance Committee."
    },
    "findings": []
  }
}
```

**Error Response:**
```json
{
  "detail": "Invalid form response schema."
}
```

### POST /api/v1/workflow
**Success Response:**
```json
{
  "id": "876f4567-e89b-12d3-a456-426614174000",
  "status": "complete",
  "intelligence": {
    "executive_summary": {
      "most_critical_bottleneck": "Manual Handoffs",
      "primary_root_cause": "Legacy system disconnect",
      "highest_priority_intervention": "Automate data entry",
      "workflow_risk_level": "High",
      "workflow_maturity": "Low"
    },
    "bottlenecks": []
  }
}
```

**Error Response:**
```json
{
  "detail": "Workflow execution failed."
}
```

### POST /api/v1/risk
**Success Response:**
```json
{
  "risk_level": "Elevated",
  "risk_score": 65,
  "risk_trend": "Stable",
  "confidence": 90,
  "explanation": "Risk is elevated because governance maturity is moderate.",
  "risk_drivers": ["Governance maturity gap"],
  "risk_timeline": {
    "near_term": [],
    "mid_term": ["Governance and adoption gaps begin affecting execution quality."],
    "long_term": []
  }
}
```

**Error Response:**
```json
{
  "detail": "Invalid dimension scores."
}
```

### POST /api/v1/failure-intelligence
**Success Response:**
```json
[
  {
    "pattern": "Governance Vacuum",
    "severity": "Critical",
    "confidence": 100,
    "why_detected": "Governance score is critically low (40/100).",
    "root_causes": ["No formal governance ownership"],
    "consequences": ["Severe compliance risk and legal exposure"],
    "recommended_actions": [
      {
        "intervention": "Establish an AI Governance Committee",
        "impact": "High",
        "effort": "Medium"
      }
    ]
  }
]
```

**Error Response:**
```json
{
  "detail": "Invalid score inputs."
}
```

---

## Security Considerations

1. **Authentication Requirements:** API consumers require a mechanism (e.g., Bearer API Keys) that can reliably map to an `org_id` and `user_id`. The current implementation relies on JWT sessions tied to a frontend UI, which is unacceptable for a third-party developer API.
2. **Data Exposure Risks:** Stateful endpoints (`/audit`, `/workflow`) store organizational data. Insufficient isolation could lead to cross-tenant data leaks. Rate-limiting is essential to prevent scraping or denial-of-service against heavy computation routes.
3. **Sensitive Outputs:** Failure Intelligence and Risk Projection expose critical organizational vulnerabilities. Such insights must be transmitted securely over HTTPS and require strict authorization validation.

---

## Refactoring Requirements

### Can expose immediately
* **Prompt Improver:** The implementation is entirely stateless, relies strictly on an input -> analyze -> result paradigm, and contains no database dependencies. It is decoupled from the UI and can be exposed immediately by simply introducing API authentication.

### Needs minor refactor
* **AI Audit:** The core orchestration exists. However, the router heavily relies on an active user session. It needs a refactor to derive the `org_id` context from an API Key.
* **Workflow Diagnostic:** Similar to the Audit API, it requires context extraction from an API key.

### Needs major refactor
* **Risk Projection:** Currently architected as an internal utility function. Needs a dedicated API route, request validation schemas, and service layer mapping.
* **Failure Intelligence:** Same as Risk Projection; strictly an internal engine. Requires the creation of Pydantic models for incoming payload configurations and an exposed controller.

*Note: For all endpoints, to truly serve a third-party developer without the TarkaX UI, a robust API Key management and issuance system must be created.*

---

## Recommended API Launch Order

1. **Prompt Improver API:** Easiest external product to consume and provides immediate value with zero state management.
2. **AI Audit API:** Core business value driver, allowing external systems to run assessments and store records.
3. **Workflow Diagnostic API:** High customer value for process automation teams.
4. **Risk Projection API:** Can be launched later to provide advanced on-demand analytics.
5. **Failure Intelligence API:** A supplementary analytical layer.

**Third-Party API Readiness Test:** Can a developer use these today without the TarkaX UI?
**Answer:** **No.** All APIs (even the Prompt Improver) lack an API Key authentication mechanism. To use any endpoint today, a developer would have to spoof a UI login to obtain a JWT. The primary dependency for B2 is implementing API Key issuance and validation.