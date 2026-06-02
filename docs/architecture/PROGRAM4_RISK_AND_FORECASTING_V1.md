# Executive Summary

Program 4 introduces two critical systems to the TarkaX platform: the Risk Prioritization Engine (SEQ 15) and the Forecasting Framework v1 (SEQ 16).

The primary objective of this architecture is to answer four essential questions for the CEO:
1. What is most likely to fail?
2. What creates the biggest business impact?
3. What should leadership fix immediately?
4. What happens if nothing changes?

In alignment with the TarkaX design philosophy, these systems optimize for **decision quality over numerical precision**. TarkaX does not seek to provide an arbitrary risk score of 73.1 vs. 74.8; instead, it synthesizes intelligence from upstream engines (Capability Gaps, Contradictions, Alignment Gaps, Failure Patterns) to deliver structured, deterministic answers about where the organization's greatest exposure lies.

The Risk Prioritization Engine sits directly between the Intelligence Layers and the Decision Support Layers (Recommendations and Action Plans). It operates on the principle that risk is not a single score but an accumulated evidence that an organizational failure is likely.

The Forecasting Framework v1 strictly utilizes a deterministic, heuristic approach to project future risk based on current conditions, entirely avoiding predictive ML or TimesFM. It assumes a "cold start" (single assessment with zero history) and projects what will likely happen if the current baseline goes unaddressed.

# Risk Prioritization Engine

The Risk Prioritization Engine evaluates and ranks organizational risks based on the aggregate intelligence gathered from the preceding pipeline stages.

**Position in Pipeline:**
`Current State -> Validation -> Diagnosis -> Intelligence (Contradiction, Alignment, Failure Pattern, Capability Gap) -> Risk Prioritization -> Recommendations -> Action Plans -> Forecasting`

**Core Philosophy:**
Risk = Capability Gap + Failure Exposure + Contradiction Severity + Alignment Severity + Failure Pattern Severity + Business Criticality + Confidence Adjustment

**Goals:**
* Synthesize multiple diagnostic vectors into unified organizational risk profiles.
* Prioritize which risks demand immediate attention based on business impact and urgency.
* Act as the direct input for the Recommendation and Action Plan engines.

# Risk Taxonomy

The Risk Taxonomy operates primarily at the Level-1 Organizational Failure level, avoiding immediate deep mapping to APQC. The focus is on macro-level business categories that resonate with the C-Suite, with optional downstream mapping to Level B/C workflows.

**Level 1: Primary Organizational Risk Domains**
* **Strategic Risk:** Misalignment between organizational goals and execution capabilities.
* **Operational Risk:** Failures in daily workflows, processes, and service delivery (e.g., Procurement Workflow).
* **Governance Risk:** Lack of oversight, controls, or policy enforcement (e.g., AI Policy Management).
* **AI Adoption Risk:** Shadow AI, unmanaged deployment, or lack of AI literacy.
* **Execution Risk:** Inability to deliver projects or initiatives on time and on budget.
* **Knowledge Risk:** Information silos, lack of documentation, or single points of failure in expertise.
* **Compliance Risk:** Regulatory exposure, data privacy violations, or audit failures.
* **Workforce Risk:** Burnout, high friction, disengagement, or lack of capability.
* **Technology Risk:** Technical debt, system instability, or architectural bottlenecks.
* **Transformation Risk:** High friction in change management or misalignment across leadership levels.

*Note: APQC mapping is an optional, secondary attribute tied to the risk, not the organizing principle.*

# Risk Scoring Model

The scoring model is 100% deterministic and relies on predefined weights applied to the outputs of the upstream diagnostic engines.

**Weighting Dimensions:**
* **Business Impact (30%):** The magnitude of consequences if the failure occurs (derived from Criticality).
* **Failure Exposure (25%):** The current vulnerability level based on capability gaps and failure patterns.
* **Likelihood (20%):** The probability of failure materializing, heavily influenced by contradiction and alignment severities.
* **Organizational Reach (15%):** The blast radius across departments, workflows, or roles.
* **Urgency (10%):** The timeline in which the failure is expected to materialize.

**Confidence Adjustment:**
The base risk score is modulated by the **Confidence Index** of the underlying findings.
* High Confidence (e.g., 80-100%) = Retain calculated severity.
* Low Confidence (e.g., < 50%) = Down-weight the overall risk priority. TarkaX must not claim high certainty or trigger "Critical Business Rescue" responses when evidence quality is weak.

# Risk Ranking Logic

Risks are ranked qualitatively into four tiers to support executive decision-making. Continuous numerical scores are strictly internal mechanisms used to sort the findings into these bands.

**Ranking Tiers:**
1. **Critical:** Imminent threat of failure. Poses severe business impact. Demands immediate executive intervention. (P0)
2. **High:** Substantial failure exposure. Requires structured remediation planning within 30 days. (P1)
3. **Medium:** Developing risk. Monitor and address through standard operational improvements. (P2)
4. **Low:** Acceptable or isolated risk. No immediate action required; track for deterioration. (P3)

*Note: Any risk with a Low Confidence Index is capped at a "High" tier (P1) and can never trigger a "Critical" (P0) alert.*

# Forecasting Framework

The Forecasting Framework v1 is a 100% deterministic, rules-based engine. It answers the question: *If current conditions persist, what is likely to happen next?*

**Constraints for V1:**
* No historical time-series data is assumed (operates on a single assessment).
* No Machine Learning (ML), TimesFM, or statistical predictive modeling.
* Utilizes forward-looking risk projections based on heuristic combinations of current state intelligence.

**Example Heuristics:**
* `High Governance Gap + High Contradiction Score + Low Confidence -> Elevated Governance Failure Risk`
* `High Alignment Gap + High Workforce Friction -> Elevated Transformation Failure Risk`
* `Critical Capability Gap in Execution + High Complexity -> Operational Bottleneck within 3-6 months`

# Forecastable Metrics

For V1, TarkaX will forecast directional trends and qualitative outcomes rather than precise numerical values.

**Core Forecast Categories:**
1. **Workflow Delays / Operational Bottlenecks:** Likelihood of process slowdowns due to execution gaps.
2. **Governance Failures:** Probability of compliance breaches or policy violations.
3. **Employee Friction / Workforce Disengagement:** Expected increase in turnover or internal resistance.
4. **Adoption Decline:** Likelihood of failed transformation or new technology (e.g., AI) rejection.
5. **Risk Escalation:** Probability that a "High" risk will deteriorate into a "Critical" risk within 6-12 months.

# Data Requirements

Because V1 does not rely on longitudinal data, it requires comprehensive input from the current assessment state:
* Output from Capability Gap Engine (What is missing?)
* Output from Alignment Engine (Where do leadership and employees disagree?)
* Output from Contradiction Engine (Where does evidence contradict claims?)
* Output from Failure Pattern Engine (What symptoms are present?)
* Current Risk Prioritization Outputs (What is the current severity?)
* Demographic Context (Industry, Organization Size, Department).

# Forecast Confidence

Forecasts are inherently uncertain, especially without historical data. The Forecast Confidence model modulates the assertiveness of the projections.

* **Base Forecast Confidence:** Inherited from the Assessment Confidence Index.
* **Deterioration Rule:** The longer the forecast horizon (e.g., 12 months vs. 3 months), the lower the forecast confidence.
* **Output Formatting:** Forecasts with low confidence use softer language (e.g., "Potential for deterioration") rather than absolute claims ("Will result in failure").

# Integration With Existing TarkaX Systems

**Inputs (Upstream Systems):**
* Receives intelligence objects from: Capability Gap Engine, Contradiction Engine, Alignment Engine, Failure Pattern Engine.
* Reads the Assessment Confidence Index.

**Outputs (Downstream Systems):**
* **Recommendation Engine:** Uses the Risk Ranking to determine the priority (P0-P3) of synthesized recommendations.
* **Action Plan Engine:** Uses Risk Urgency to sequence action items (Immediate, 30-Day, 60-Day, 90-Day).
* **Forecasting Framework:** Uses Risk Scores and Intelligence vectors to project deterioration.

# Exact Backend Components Needed

* `RiskPrioritizationEngine`: Service class responsible for computing weighted risk scores and assigning Critical/High/Medium/Low tiers based on upstream intelligence vectors.
* `ForecastHeuristicEngine`: Deterministic rules engine executing IF-THEN heuristic logic to map current-state combinations to future projections.
* `ConfidenceAdjuster`: Utility module to down-weight risk severity and soften forecast language based on validation confidence.
* `RiskTaxonomyMapper`: Module to classify raw findings into the Level-1 Organizational Risk Domains.

# Exact Database Changes Needed

* **Table: `risk_assessments`**
  * `id` (UUID, PK)
  * `assessment_id` (UUID, FK)
  * `risk_domain` (Enum: Strategic, Operational, Governance, etc.)
  * `impact_score` (Numeric)
  * `likelihood_score` (Numeric)
  * `exposure_score` (Numeric)
  * `urgency_score` (Numeric)
  * `reach_score` (Numeric)
  * `confidence_adjustment` (Numeric)
  * `final_risk_tier` (Enum: Critical, High, Medium, Low)
  * `underlying_findings` (JSONB list of references to upstream engine outputs)

* **Table: `forecast_projections`**
  * `id` (UUID, PK)
  * `assessment_id` (UUID, FK)
  * `forecast_metric` (Enum: Workflow Delays, Governance Failures, etc.)
  * `projected_outcome` (Text / Enum)
  * `time_horizon` (Enum: 3-Months, 6-Months, 12-Months)
  * `triggering_heuristics` (JSONB mapping of what caused the forecast)
  * `forecast_confidence` (Numeric)

# Exact Future API Requirements

* `POST /api/v1/engines/risk/calculate`
  * Triggers the Risk Prioritization Engine for a given `assessment_id`.
* `GET /api/v1/assessments/{id}/risks`
  * Retrieves the ranked list of risks, filtered by tier or domain.
* `POST /api/v1/engines/forecast/project`
  * Triggers the Forecasting Framework for a given `assessment_id`.
* `GET /api/v1/assessments/{id}/forecasts`
  * Retrieves the deterministic projections and potential deterioration metrics.

# Effort Estimate

* **Risk Prioritization Engine Development:** 2-3 Weeks (Defining weights, building the calculator, and mapping to taxonomy).
* **Forecasting Framework v1 Development:** 2-3 Weeks (Defining the deterministic heuristic matrix and implementing the rules engine).
* **Database & API Integration:** 1 Week.
* **Testing & Tuning:** 1-2 Weeks (Calibrating the weights to ensure Low Confidence never triggers P0, and verifying decision support outputs).
* **Total Estimated Effort:** 6-9 Weeks for full architectural realization.