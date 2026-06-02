# PROGRAM 5: REPORTING PLATFORM ARCHITECTURE

## Context & Objectives
TarkaX is an Organizational Failure Intelligence Platform, not a survey platform. The Reporting Platform (Layer 6) is the final presentation tier designed strictly for decision-makers. It operates on a singular principle: **every section must empower the reader to make a specific, high-stakes decision.**

The report eschews simplistic "Score → Graph → PDF" paradigms. Instead, it follows a rigorous intelligence pipeline:
**Evidence → Diagnosis → Root Cause → Risk → Recommendation → Forecast → Action Plan.**

## PART 1: REPORT V2 ARCHITECTURE (UNIFIED MODULAR FRAMEWORK)

### 1.1 Core Philosophy
We will not build 18 separate report templates. TarkaX utilizes a **Unified Modular Reporting Framework**.

**Architecture Flow:**
`Core Intelligence Engine (L2-L5) → Audience Context Layer → Assessment Layer → Dynamic Report Composition`

A single finding is dynamically adapted to the audience:
* **Executive:** Focuses on business impact and strategic risk.
* **Consultant:** Focuses on structural root causes, capability gaps, and implementation nuances.
* **Government:** Focuses on governance, policy adherence, and systemic compliance exposure.

### 1.2 Audience Profiles & Dynamic Output

#### A. Executive View
* **Purpose:** To answer "Is my company failing, how much will it cost, and what must I do today?"
* **Audience:** C-Suite, Board of Directors.
* **Sections:** Executive Summary, P0 Risks, Strategic Interventions, ROI of Action vs. Cost of Inaction.
* **Insights:** High-level, impact-driven, zero jargon.
* **Visualizations:** Risk exposure heatmaps, capability vs. maturity radar.
* **Required Inputs:** L5 Action Plan, L4 Risk & Forecasting Engine.

**Consulting-Grade Narrative Examples (Executive):**
* **Insight:** "Your execution teams are operating in a 'Shadow AI' environment. While leadership believes AI adoption is strictly governed, 42% of core delivery workflows rely on unsanctioned tools."
* **Root Cause:** "The failure is not technological; it is structural. The organization lacks an operational translation layer between executive policy and daily execution."
* **Risk:** "Continued misalignment carries a Critical (P0) risk of a severe data exfiltration event within 6 months, representing an estimated $3.2M financial exposure."
* **Recommendation:** "Immediately mandate a unified AI workflow ontology and freeze unsanctioned tooling at the departmental level."
* **Forecast:** "If no action is taken, the probability of a critical vendor compliance breach increases to 85% by Q3."
* **Action Plan:** "Immediate (Day 1-15): CIO to execute a complete audit of unauthorized AI endpoints. Immediate (Day 15-30): COO to draft explicit acceptable use policies mapped to APQC frameworks."

#### B. Consultant View
* **Purpose:** To provide a deep, defensible diagnostic blueprint that a consulting partner can present to a client to justify an engagement.
* **Audience:** Big 4 Partners, Management Consultants, Enterprise Architects.
* **Sections:** Diagnostic Findings, Root Cause Analysis, Capability Gap Deep-Dive, Transformation Sequencing.
* **Insights:** Granular, structural, APQC-aligned.
* **Visualizations:** Process breakdown charts, Contradiction Engine matrices (Leadership vs. Employee perception gaps).
* **Required Inputs:** L3 Root Cause Engine, L4 Capability Gap Engine, L2.5 Contradiction Engine.

**Consulting-Grade Narrative Examples (Consultant):**
* **Insight:** "Asymmetric communication between the executive layer and execution teams has created a 45% reality gap, obscuring critical delays in the Order-to-Cash core workflow."
* **Root Cause:** "Systemic reliance on implicit cultural knowledge for cross-departmental handoffs rather than explicit governance frameworks, resulting in a systemic bottleneck when scaling beyond 500 employees."
* **Risk:** "Operational paralysis during the upcoming Q4 ERP migration due to undocumented legacy interdependencies."
* **Recommendation:** "Transition from siloed, tool-specific governance to a unified workflow ontology. Implement an explicit sign-off matrix for Layer B APQC processes."

#### C. Government View
* **Purpose:** To ensure strict alignment with public sector mandates, emphasizing compliance, oversight, and policy adherence.
* **Audience:** Agency Directors, Compliance Officers, Public Sector Auditors.
* **Sections:** Policy Alignment, Governance Gaps, Systemic Risk Exposure, Remediation Roadmap.
* **Insights:** Bureaucratic, policy-driven, highly structured.
* **Visualizations:** Compliance matrices, policy-to-action mapping.
* **Required Inputs:** L4 Intelligence Engine, L5 Action Plan Engine.

**Consulting-Grade Narrative Examples (Government):**
* **Insight:** "Departmental operations are currently disjointed; the implementation of Directive 8140 is fragmented across three disjointed sub-agencies without a central oversight mechanism."
* **Action Plan:** "Immediate (30-Day): Appoint a centralized governance task force to standardize public-facing data workflows."

### 1.3 Assessment Matrix
Regardless of the audit type (AI Audit, Workflow Diagnostic, Leadership/Manager/Employee Audit, Alignment Audit), the framework extracts standardized concepts:
* **Findings:** Raw truths extracted from L2 Validation.
* **Root Causes:** "Why did this fail?" (L3 Engine).
* **Risks:** "How bad is this?" (L4 Engine).
* **Benchmarks:** "What does good look like?" (L4 Engine).
* **Recommendations:** "What is the structural fix?" (L5 Engine).
* **Forecasts:** "What happens if we do nothing?" (L4 Engine).
* **Action Plans:** "Who does what, and when?" (L5 Engine).

---

## PART 2: EXECUTIVE DASHBOARD

The dashboard is built entirely around decisions, eschewing vanity metrics and arbitrary score-chasing.

### Level 1: Single Assessment View (The Snapshot)
Designed to quickly orient an executive on a specific diagnostic run.

#### Section 1: "What is wrong?" (Reality Gap & Critical Failures)
* **Purpose:** Forces the executive to confront failure instantly without sugarcoating.
* **Inputs:** Contradiction Engine (L2.5), Capability Gap Engine (L4).
* **Outputs:** Highest severity capability gaps and cross-persona contradictions.
* **Visual Components:** Contradiction Matrix (Leadership Perception vs. Ground Truth Reality).
* **Decision:** "Where must I direct my attention immediately?"

#### Section 2: "Why is it happening?" (Root Cause Intelligence)
* **Purpose:** Shifts the conversation from symptoms (e.g., "sales are down") to structural diseases (e.g., "lack of a unified CRM ontology").
* **Inputs:** Root Cause Engine (L3).
* **Outputs:** Synthesized structural failures.
* **Visual Components:** Root Cause Dependency Tree.
* **Decision:** "Which fundamental systems need restructuring?"

#### Section 3: "What should we do?" (Strategic Interventions)
* **Purpose:** Provides definitive, sequenced actions rather than generic advice.
* **Inputs:** Recommendation Engine (L5), Action Plan Engine (L5.5).
* **Outputs:** Prioritized interventions by Business Impact and Risk Severity.
* **Visual Components:** Intervention ROI vs. Implementation Effort scatterplot.
* **Decision:** "Which initiative do I fund today?"

### Level 2: Organizational Trend View (The Trajectory)
Designed to track systemic health over time across multiple assessments.

#### Section 4: "Are we improving?" (Capability Trend)
* **Purpose:** Tracks the actual closure of capability gaps, not arbitrary assessment scores.
* **Inputs:** Capability Gap Engine (L4) historical data.
* **Outputs:** Movement across the 5-level maturity model (Fragile → Resilient).
* **Visual Components:** Longitudinal Maturity Tracking.
* **Decision:** "Is our transformation budget actually generating capability?"

#### Section 5: "Where are risks increasing?" (Risk Velocity)
* **Purpose:** Identifies deteriorating departments before they fail.
* **Inputs:** Risk Engine (L4).
* **Outputs:** Departments or workflows with the highest negative momentum.
* **Visual Components:** Heatmap of deteriorating workflows (APQC aligned).
* **Decision:** "Where do I need to preemptively intervene?"

#### Section 6: "What happens if we do nothing?" (Cost of Inaction)
* **Purpose:** Quantifies the financial and operational penalty of ignoring the intelligence.
* **Inputs:** Forecasting Engine (L4).
* **Outputs:** Projected severity and probability of specific failure events.
* **Visual Components:** Failure Probability Curve over time (0-18 months).
* **Decision:** "Can I afford to delay this transformation?"

---

## PART 3: PDF ARCHITECTURE

One PDF architecture, dynamically modulated for three audience profiles (Executive, Consultant, Government).

### 3.1 Page Structure & Requirements

#### 1. Executive Summary
* **Why it exists:** The CEO will only read this page. It must deliver the lethal truth immediately.
* **Data Source:** Synthesized L4/L5 highest priority outputs.
* **Example:** "Your organization suffers from a 40% Reality Gap. Leadership believes AI is governed; evidence proves shadow AI is rampant. If unresolved, expect a critical compliance breach by Q3. Immediate remediation requires $400k in structural transformation."

#### 2. Findings & Contradictions
* **Why it exists:** To validate that the assessment actually found real data and isn't hallucinating.
* **Data Source:** L2 Validation, L2.5 Contradiction Engine.
* **Example:** "Finding: 80% of Managers claim standardized workflows exist. Contradiction: 0% of Employees provided valid evidence of workflow documentation."

#### 3. Root Causes
* **Why it exists:** To prevent the client from fixing symptoms instead of the actual disease.
* **Data Source:** L3 Root Cause Engine.
* **Example:** "Root Cause: Siloed operational knowledge due to an absence of an APQC Layer B governance framework, leading to extreme dependency on key personnel."

#### 4. Risks & Forecasts (Cost of Inaction)
* **Why it exists:** To create urgency and justify the budget required for the recommendations.
* **Data Source:** L4 Risk & Forecasting Engine.
* **Example:** "Risk: Attrition of the VP of Sales will cause a total collapse of the Q3 pipeline because institutional knowledge is entirely un-digitized. Probability: 85% within 12 months."

#### 5. Benchmarking & Capability Gaps
* **Why it exists:** To define "what good looks like" specific to their industry/size, stripping away vanity metrics.
* **Data Source:** L4 Capability Gap Engine.
* **Example:** "Target State: Level 3 (Operational). Current State: Level 1 (Fragile). Gap: Missing explicit Vendor Onboarding workflows."

#### 6. Recommendations & Transformation
* **Why it exists:** To map the structural intervention required to solve the capability gap.
* **Data Source:** L5 Recommendation Engine.
* **Example:** "Intervention P0: Deploy centralized workflow taxonomy across all cross-functional revenue teams."

#### 7. 30/60/90-Day Action Plans
* **Why it exists:** To transition from theory to execution, assigning specific tasks to abstract roles.
* **Data Source:** L5 Action Plan Engine.
* **Example:** "30-Day: COO to mandate freeze on unauthorized SaaS procurement. 60-Day: Enterprise Architect to draft Target State architecture."

#### 8. Appendices
* **Why it exists:** For the technical practitioners who demand to see the raw evidence and APQC mappings.
* **Data Source:** Raw L1 Assessment Data, APQC Normalization Data.

---

## PART 4: REPORT DATA CONTRACT

### Conceptual Mapping

```text
ENGINE                            OUTPUT                              REPORT SECTION
---------------------------------------------------------------------------------------------------
Layer 2 Validation           →  Validated Evidence             →  Appendices / Audit Details
Layer 2.5 Contradiction      →  Reality Gaps                   →  Executive Summary / Findings
Layer 3 Root Cause           →  Structural Failures            →  Root Causes
Layer 4 Intelligence         →  Severity, Exposure, Maturity   →  Risks / Benchmarks
Layer 5 Decision Support     →  Interventions & Sequencing     →  Recommendations / Action Plans
Layer 6 Reporting            →  Dynamic Document Composition   →  PDF & Dashboard
```

### Technical Representation (REPORT_DATA_MODEL_V1)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TarkaX Report Data Model V1",
  "type": "object",
  "properties": {
    "report_context": {
      "type": "object",
      "properties": {
        "assessment_id": { "type": "string", "format": "uuid" },
        "audience_profile": { "type": "string", "enum": ["executive", "consultant", "government"] },
        "assessment_type": { "type": "string", "enum": ["ai_audit", "workflow_diagnostic", "alignment_audit"] },
        "organization_demographics": { "type": "object" }
      },
      "required": ["assessment_id", "audience_profile", "assessment_type"]
    },
    "executive_summary": {
      "type": "object",
      "properties": {
        "primary_insight_narrative": { "type": "string" },
        "critical_risk_count": { "type": "integer" },
        "organizational_reality_gap_percentage": { "type": "number" },
        "cost_of_inaction_narrative": { "type": "string" }
      }
    },
    "intelligence_payload": {
      "type": "object",
      "properties": {
        "contradictions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "perception_gap": { "type": "string" },
              "evidence_reality": { "type": "string" },
              "severity": { "type": "string", "enum": ["low", "medium", "high", "critical"] }
            }
          }
        },
        "root_causes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "symptom": { "type": "string" },
              "structural_disease": { "type": "string" },
              "apqc_mapping": { "type": "string" }
            }
          }
        },
        "capability_gaps": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "capability_name": { "type": "string" },
              "current_maturity": { "type": "string", "enum": ["L1_Fragile", "L2_Emerging", "L3_Operational", "L4_Scaled", "L5_Resilient"] },
              "target_maturity": { "type": "string" }
            }
          }
        },
        "risks_and_forecasts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "failure_event": { "type": "string" },
              "probability": { "type": "number" },
              "time_horizon": { "type": "string" },
              "impact_narrative": { "type": "string" }
            }
          }
        }
      }
    },
    "decision_support": {
      "type": "object",
      "properties": {
        "recommendations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "intervention_title": { "type": "string" },
              "strategic_rationale": { "type": "string" },
              "priority_level": { "type": "string", "enum": ["P0", "P1", "P2", "P3"] }
            }
          }
        },
        "action_plan": {
          "type": "object",
          "properties": {
            "immediate_30_days": { "type": "array", "items": { "type": "string" } },
            "short_term_60_days": { "type": "array", "items": { "type": "string" } },
            "long_term_90_days": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    }
  },
  "required": ["report_context", "executive_summary", "intelligence_payload", "decision_support"]
}
```

---

## PART 5: CONSULTING DELIVERABLE TEST

**Test Criteria:** Would a Big 4 consulting firm confidently hand this report to a paying client? Would a CEO learn something they did not already know?

**Verdict:** YES.

**Justification:**
1. **Decision-Centric over Data-Centric:** The architecture forcefully prevents "dashboard spam" (meaningless charts). It answers C-suite questions directly (What is broken? Why? What do I do? What happens if I ignore it?).
2. **Organizational Reality Check:** By elevating Contradictions (Reality Gaps) to the Executive Summary, the platform instantly breaks through leadership echo chambers. Telling a CEO "Your team thinks everything is fine, but the evidence proves it isn't" is consulting gold.
3. **Actionable Accountability:** The report does not end with "Improve Communication." It ends with explicit 30/60/90-day mandates assigned to executive roles, creating immediate operational friction and accountability.
4. **Defensible Intelligence:** Because every Risk and Forecast is traced back to a Root Cause, and every Root Cause is traced back to Validated Evidence, the consultant cannot be easily dismissed by a defensive executive. The evidence chain is bulletproof.

---

## PART 6: EXACT FUTURE FILES IMPACTED

To implement this architecture in the future, the following files will be created or heavily modified:

* `backend/schemas/report_data_model.py` (Implementation of the JSON Schema)
* `backend/api/routers/reports.py` (Endpoints for report generation and dynamic views)
* `backend/services/reporting/composition_engine.py` (Core logic for adapting L2-L5 data into the Audience View)
* `frontend/components/dashboard/ExecutiveDashboard.tsx` (Level 1 & Level 2 views)
* `frontend/components/dashboard/RealityGapMatrix.tsx` (Visual component for contradictions)
* `frontend/services/pdf/DynamicPdfGenerator.ts` (Dynamic template engine for PDF V2)

---

## PART 7: IMPLEMENTATION COMPLEXITY ESTIMATE

* **Data Contract & Backend Assembly:** Moderate. The JSON schema is highly structured, but synthesizing the outputs from L2-L5 into a coherent narrative payload will require robust mapping logic.
* **Dynamic PDF Generation:** High. Building a PDF engine that doesn't just inject text, but logically restructures document flow based on audience context, is notoriously difficult. Will likely require a sophisticated headless browser/React-to-PDF pipeline.
* **Executive Dashboard:** Moderate to High. Level 1 (Single Assessment) is straightforward. Level 2 (Trend/Longitudinal Analysis) requires complex state management and historical data querying across potentially disparate assessment schemas over time.
* **Overall Assessment:** This is a heavy architectural lift (estimated 4-6 weeks for an MVP implementation of Layer 6), primarily due to the stringent requirement for cohesive narrative synthesis over simplistic data dumping.
