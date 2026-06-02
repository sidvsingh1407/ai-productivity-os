# TarkaX Action Plan Engine v1: Architectural Blueprint

## 1. Executive Summary

As TarkaX evolves into a premier Organizational Failure Intelligence Platform, generating raw diagnostic outputs is insufficient. Enterprise clients—and the consulting firms that serve them (McKinsey, BCG, Deloitte)—require actionable, structured, and sequenced transformation blueprints.

The **Action Plan Engine v1 (Layer 5.5)** bridges the critical gap between "What should be fixed?" (Recommendations) and "How should it be fixed?" (Implementation). Sitting logically between the Recommendation Engine and Reporting Layer, it translates structural recommendations and capability gaps into deterministic, highly sequenced 30/60/90-day action plans.

This engine is fundamentally **deterministic**—relying on a rules-based Action Library to ensure consistent, consulting-grade outputs. AI is strictly relegated to a secondary formatting and explanatory role, ensuring that TarkaX delivers strategy, not LLM hallucinations. The engine acts as a bridge from identified Root Causes and missing Capabilities to specific, time-bound interventions with defined owners, dependencies, and business impact.

---

## 2. Engine Architecture & Pipeline Placement

### Pipeline Placement

The Action Plan Engine operates downstream of the Recommendation Engine. It consumes aggregated intelligence to build an operational timeline.

`L0 Collection` → `L1 Assessment` → `L2 Validation` → `L3 Root Cause` → `L4 Capability Gap` → `L5 Recommendation` → **`L5.5 ACTION PLAN ENGINE`** → `L6 Reporting`

### Core Principles

1.  **Deterministic Primary Layer:** Findings map to a rules engine which queries an Action Library.
2.  **LLM Secondary Layer:** Only *after* the structured timeline is constructed deterministically does an LLM intervene to refine tone, rewrite descriptions for executive context, or generate summary narratives. The LLM **never** dictates the core plan logic.
3.  **Capability-Centric:** The engine resolves Capability Gaps. It does not merely generate a list of to-dos; it sequences the operational steps necessary to build a missing capability.
4.  **Role-Based Ownership:** Actions are assigned to functional roles (e.g., COO, AI Governance Head), not named individuals.

### The Transformation Chain

The engine's logic follows a strict synthesis path:
`Root Cause` → `Capability Gap` → `Recommendation` → `Sequenced Action Timeline`

---

## 3. Input Model

The Action Plan Engine requires a comprehensive payload synthesized from upstream layers.

### Upstream Intelligence Inputs

*   **Assessment & Validation:** Verified input data and Confidence Index scores.
*   **Root Cause Analysis:** "Why is this happening?" (e.g., *Absence of centralized AI Governance*).
*   **Capability Gap (Benchmark/Failure Patterns):** "What capability is missing?" (e.g., *Missing AI Policy Framework*).
*   **Risk & Contradiction Scores:** "What is the exposure?" (e.g., *High Risk of Shadow AI*).
*   **Recommendation:** "What should be fixed?" (e.g., *Implement centralized AI Governance Framework*).

### Action Synthesis Object (Pre-Processing)

```json
{
  "finding_id": "F-8842",
  "root_cause": "No centralized oversight for generative AI tools.",
  "capability_gap": "AI Governance & Policy Management",
  "risk_severity": "Critical",
  "recommendation": "Implement Centralized AI Governance Framework",
  "target_audience_demographics": {
    "industry": "Financial Services",
    "size": "Enterprise"
  }
}
```

---

## 4. Output Model

The engine produces a structured transformation roadmap designed to immediately slot into a consulting firm's delivery framework.

### Action Object Structure

For every sequenced action, the output must rigidly define:

1.  **Action Title:** A clear, active-verb directive.
2.  **Why It Matters:** The strategic imperative (mapped back to Root Cause).
3.  **Expected Benefit:** The measurable operational outcome.
4.  **Dependencies:** Pre-requisite actions or conditions.
5.  **Owner Role:** Target persona (e.g., CEO, CIO, Department Head).
6.  **Priority Level:** P0 to P3 (Calculated by the Prioritization Framework).

### The Action Plan Payload (Post-Processing)

```json
{
  "recommendation_id": "REC-901",
  "capability_gap_addressed": "AI Governance & Policy Management",
  "plan_overview": "A 90-day structural plan to establish and enforce AI usage policies.",
  "timeline": {
    "immediate": [ { /* Action Object */ } ],
    "day_30": [ { /* Action Object */ } ],
    "day_60": [ { /* Action Object */ } ],
    "day_90": [ { /* Action Object */ } ]
  }
}
```

---

## 5. Prioritization Framework

Action sequencing and recommendation ranking are fundamentally different problems. While a recommendation might be Critical (P0), its subsequent 90-day actions might range from P0 to P2 depending on urgency.

The Action Plan Engine utilizes a distinct, weighted calculation model to assign priority (P0 - P3) to individual actions.

### Weighting Model

*   **Risk Severity (25%):** How quickly will failure occur without this action? (Higher risk = Immediate/P0).
*   **Business Impact (25%):** Value created or protected by executing this step.
*   **Time To Value (20%):** Speed of ROI. Faster time-to-value pushes items to Immediate/30-Day tiers.
*   **Dependency Complexity (15%):** Actions with many downstream dependents receive higher priority to unblock workflows.
*   **Implementation Effort (10%):** Lower effort items are prioritized earlier (Quick Wins).
*   **Confidence Level (5%):** Modulator based on validation scores. Low confidence downgrades priority.

### Priority Bands

*   **P0 (Critical):** Immediate business rescue, compliance mandates, or critical unblockers. (Score: 90-100)
*   **P1 (High):** Structural foundations required for the capability gap. (Score: 75-89)
*   **P2 (Medium):** Operational optimizations and scaling actions. (Score: 50-74)
*   **P3 (Low):** Long-term refinement, edge-case documentation. (Score: <50)

---

## 6. Action Categories

Actions are strictly categorized into an APQC-aligned operational taxonomy. This allows filtering and aggregation by department (e.g., "Show me all 30-Day Governance actions").

*   **Governance:** Frameworks, steering committees, oversight boards.
*   **Workflow Optimization:** Process re-engineering, bottleneck elimination.
*   **Process Standardization:** SOP creation, baseline definitions.
*   **Documentation:** Artifact generation, runbooks, architecture diagrams.
*   **Knowledge Management:** Centralizing IP, taxonomy creation, searchability.
*   **AI Adoption:** Tool provisioning, use-case mapping, model deployment.
*   **Automation:** RPA, scripting, integration pipelines.
*   **Training & Enablement:** Upskilling, change management workshops, onboarding.
*   **Compliance:** Audits, regulatory alignment, data privacy checks.
*   **Risk Management:** Threat modeling, mitigation planning.
*   **Operational Visibility:** Dashboards, telemetry, tracking.
*   **Performance Management:** Incentive alignment, reviews.
*   **Decision-Making:** Authority matrices (RACI), approval workflows.
*   **Communication:** Internal comms, stakeholder alignment.
*   **Technology Consolidation:** Sunsetting tools, technical debt reduction.
*   **Change Management:** Cultural adoption, resistance mitigation.
*   **Capacity Management:** Resource modeling, workload balancing.
*   **Resource Allocation:** Budgeting, headcount mapping.
*   **Vendor Management:** SLA reviews, procurement.
*   **Data Quality:** Cleansing, master data management.
*   **Measurement & KPIs:** Metric definition, OKR alignment.

---

## 7. Plan Generation Logic (30/60/90-Day Sequencing)

The Engine places actions into distinct time horizons based on Dependency Logic and the Prioritization Score.

### Immediate Actions (Days 0-14)
*   **Profile:** "Quick Wins" & "Bleeding Necks".
*   **Logic:** High Risk + High Time To Value + Low Effort. Actions required to stop immediate failure or establish absolute prerequisites (e.g., appointing an owner).

### 30-Day Actions (Days 15-30)
*   **Profile:** "Foundational Changes".
*   **Logic:** Discovery, baselining, and policy drafting. Establishing the architecture for the missing capability.

### 60-Day Actions (Days 31-60)
*   **Profile:** "Structural Execution".
*   **Logic:** Rollout, pilot programs, and integration. Moving from theory to practice within bounded environments.

### 90-Day Actions (Days 61-90)
*   **Profile:** "Scaling & Measurement".
*   **Logic:** High Implementation Effort + High Impact. Operationalizing across the enterprise, measuring KPIs, and standardizing.

---

## 8. Example Outputs

### Example 1: AI Audit
**Scenario:** An organization is using generative AI without oversight.
*   **Root Cause:** No AI Governance Owner.
*   **Capability Gap:** AI Policy Framework.
*   **Recommendation:** Implement Centralized AI Governance.

**Action Plan:**
*   **Immediate (P0):** Identify and appoint an Executive AI Governance Sponsor.
    *   *Why:* To establish accountability. *Owner:* CEO.
*   **30-Day (P1):** Draft Interim Acceptable Use Policy for Generative AI.
    *   *Why:* To mitigate immediate Shadow AI risk. *Owner:* Legal/CIO.
*   **60-Day (P1):** Conduct shadow AI discovery audit across all departments.
    *   *Why:* To map actual usage. *Owner:* IT Team.
*   **90-Day (P2):** Operationalize AI Review Board for new tool procurement.
    *   *Why:* To establish long-term gatekeeping. *Owner:* AI Steering Committee.

### Example 2: Workflow Diagnostic
**Scenario:** A client onboarding process takes 45 days instead of 10.
*   **Root Cause:** Manual data entry across 4 disconnected legacy systems.
*   **Capability Gap:** Process Automation & Integration.
*   **Recommendation:** Automate Data Ingestion via API integrations.

**Action Plan:**
*   **Immediate (P1):** Map current state "As-Is" onboarding workflow.
    *   *Why:* To identify exact integration points. *Owner:* Process Analyst.
*   **30-Day (P1):** Standardize data intake template for all new clients.
    *   *Why:* To normalize data before automation. *Owner:* Ops Head.
*   **60-Day (P2):** Pilot API integration between CRM and Billing system.
    *   *Why:* To eliminate the primary manual entry bottleneck. *Owner:* IT Architecture.
*   **90-Day (P2):** Retire legacy data entry portal and train staff on automated flow.
    *   *Why:* To realize ROI and enforce adoption. *Owner:* Training/Ops.

### Example 3: Leadership Audit
**Scenario:** The executive team is pursuing contradictory strategic goals.
*   **Root Cause:** Fragmented KPI definitions at the C-level.
*   **Capability Gap:** Strategic Alignment & Measurement.
*   **Recommendation:** Implement Unified OKR Framework.

**Action Plan:**
*   **Immediate (P0):** Schedule cross-functional Executive Alignment Offsite.
    *   *Why:* To expose contradictions in a unified forum. *Owner:* CEO/Chief of Staff.
*   **30-Day (P1):** Define 3 macro-level Company Objectives for the year.
    *   *Why:* To restrict scope creep. *Owner:* Executive Team.
*   **60-Day (P1):** Cascade top-level OKRs to Department Heads.
    *   *Why:* To create operational linkage. *Owner:* Department Managers.
*   **90-Day (P2):** Implement quarterly OKR review rhythm into existing leadership meetings.
    *   *Why:* To ensure sustained alignment. *Owner:* PMO / Chief of Staff.

### Example 4: Employee Audit
**Scenario:** High turnover in customer success due to burnout and lack of tooling.
*   **Root Cause:** Lack of standard operating procedures leading to ad-hoc firefighting.
*   **Capability Gap:** Process Documentation & Knowledge Management.
*   **Recommendation:** Centralize Customer Success Knowledge Base.

**Action Plan:**
*   **Immediate (P1):** Appoint a Knowledge Champion within the CS Team.
    *   *Why:* To drive documentation accountability. *Owner:* CS Director.
*   **30-Day (P1):** Identify Top 10 most frequent customer escalations.
    *   *Why:* To prioritize documentation efforts. *Owner:* Knowledge Champion.
*   **60-Day (P2):** Create and publish standardized SOPs for the Top 10 escalations.
    *   *Why:* To reduce ad-hoc problem solving. *Owner:* Subject Matter Experts.
*   **90-Day (P2):** Integrate Knowledge Base search into the primary ticketing tool.
    *   *Why:* To improve Time-to-Value for agents. *Owner:* CS Ops / IT.

### Example 5: Alignment Audit
**Scenario:** Leadership believes the company is "Agile," but Engineering reports strict Waterfall constraints.
*   **Root Cause:** Misaligned perception of operational maturity (Reality Gap).
*   **Capability Gap:** Operational Visibility & Communication.
*   **Recommendation:** Re-baseline Agile Delivery Methodology.

**Action Plan:**
*   **Immediate (P0):** Present Alignment Audit contradiction data directly to Engineering VP and Product VP.
    *   *Why:* To break perception bubbles using objective evidence. *Owner:* Transformation Lead.
*   **30-Day (P1):** Define exact organizational definitions of 'Agile' and 'Done'.
    *   *Why:* To create a shared language. *Owner:* Agile Coach / Engineering VP.
*   **60-Day (P2):** Restructure cross-functional squads to empower localized decision-making.
    *   *Why:* To remove structural waterfall gates. *Owner:* Product / Engineering Leadership.
*   **90-Day (P2):** Implement standardized cycle-time metrics dashboard to provide objective visibility.
    *   *Why:* To prevent future reality gaps. *Owner:* Engineering Ops.