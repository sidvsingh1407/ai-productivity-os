# TarkaX Validation Layer (v1)

## Architecture & Intelligence Blueprint
**Strategic Owner:** Principal Product Architect & Enterprise Risk Consultant
**Status:** Design Phase

---

## EXECUTIVE SUMMARY

TarkaX is positioned as an Organizational Failure Intelligence Platform. Before delivering organizational insights—such as structural root causes, capability gaps, or benchmark alignments—TarkaX must establish deterministic confidence in the data.

The **Validation Layer (L2)** acts as the critical gatekeeper between the **Assessment Layer (L1)** and the **Diagnosis Layer (L3)**. Its sole objective is to answer: *"Can we trust the assessment data, and how confident should we be in our resulting conclusions?"*

It explicitly does not diagnose what is wrong; it evaluates whether the information provided is robust enough to diagnose anything at all.

---

## SECTION 1: VALIDATION PHILOSOPHY

### 1.1 Why Validation is Required
Assessments inherently capture subjective human input, which introduces bias, approximation, fatigue, and deliberate obfuscation. To generate enterprise-grade failure intelligence, raw inputs must be quantified for reliability. Without a Validation Layer, downstream engines risk operating on "garbage in, garbage out," rendering executive recommendations untrustworthy.

### 1.2 Why Scores Alone Are Insufficient
A raw assessment score (e.g., "75% Maturity") treats a single-word response as mathematically equal to a fully documented, artifact-backed workflow. It fails to capture the fragility of the data. Scores measure *what* is claimed, whereas validation measures the *substance* of the claim.

### 1.3 Downstream Support Capabilities
The Validation Layer is the foundational enabler for TarkaX's advanced analytical engines:
* **Root Cause Engine:** Ensures the engine investigates real organizational gaps rather than symptoms of poor data entry.
* **Benchmark Engine:** Prevents organizations from falsely matching top-tier benchmarks due to overly optimistic, unsubstantiated self-assessments.
* **Alignment Engine:** Provides the baseline "trust metric" needed when weighing conflicting answers across cohorts (e.g., Leadership vs. Employee).
* **Failure Pattern Engine:** Distinguishes between actual operational contradictions and simple user error during assessment.
* **Consultant Reports:** Equips consultants with a meta-analysis of organizational self-awareness and data maturity.

---

## SECTION 2: TRUST FRAMEWORK

### 2.1 The Assessment Trust Score
The Trust Score evaluates the **input quality** of an individual assessment. It answers: *"Is the submitted data complete, robust, and internally consistent?"*

**Scale:** 0–100

### 2.2 Core Components of the Trust Score
The Trust Score is a deterministic calculation derived from the following dimensions:
1. **Evidence Quality:** (Weight: Heavy) The depth and verifiability of claims (see Evidence Quality Levels below).
2. **Missing Data Detection:** (Weight: Heavy) Penalties for explicitly skipped questions or abandoned sections.
3. **Internal Consistency:** (Weight: Moderate) Contradictions within the *same* assessment (e.g., claiming "Fully Automated" but noting "Heavy Manual Workarounds").
4. **Response Depth:** (Weight: Moderate) The verbosity and structured completeness of open-text or multi-select responses.

### 2.3 Evidence Quality Levels
To programmatically assess evidence, TarkaX employs a 5-level maturity model for substantiation:

* **Level 1: Assertion Only** (Lowest Trust)
  * *Example: "We have an AI policy."*
* **Level 2: Assertion + Explanation**
  * *Example: "We have an AI policy that is reviewed quarterly by IT."*
* **Level 3: Assertion + Explanation + Tool Context**
  * *Example: "We have an AI policy reviewed quarterly, enforced via our Azure governance portal."*
* **Level 4: Assertion + Explanation + Tool Context + Process Ownership**
  * *Example: "We have an AI policy reviewed quarterly, enforced via Azure, managed by the VP of Engineering."*
* **Level 5: Assertion + Explanation + Tool Context + Process Ownership + Supporting Artifact** (Highest Trust)
  * *Example: Includes the above details and a validated link/upload of the policy document.*

### 2.4 Missing Data vs. Lack of Evidence
The Trust Framework makes a strict distinction between data omission and operational reality:
* **Missing Data:** A skipped question or abandoned section. This represents poor assessment completion and **reduces** the Trust Score.
* **Lack of Evidence:** The user explicitly selects "Unknown," "Not Documented," or "No Data Available." This is a valid operational reality. It is categorized as an **Evidence State** and does **not** penalize the Trust Score, as it provides high-trust intelligence about an organizational blind spot.

---

## SECTION 3: CONFIDENCE INDEX

### 3.1 The Assessment Confidence Index
If the Trust Score evaluates the input, the **Confidence Index** evaluates the **certainty of the output (conclusions)**. It answers: *"Given the Trust Score and external context, how heavily should we rely on the generated insights?"*

**Scale:** Percentage (0–100%) mapped to High, Medium, and Low tiers.

### 3.2 Methodology
The Confidence Index is influenced by the Trust Score, but modulates based on:
* **Benchmark Coverage:** Is there enough industry benchmark data to confidently compare this specific organization?
* **Historical Data Availability:** Does this organization have previous assessments to validate the current trend?
* **Organizational Complexity:** Are there unusual demographic factors (e.g., highly niche industry) that lower statistical certainty?

### 3.3 Confidence Tiers
* **High Confidence (80–100%):** High Trust Score, strong benchmark alignment, robust historical data. Downstream engines can generate definitive recommendations.
* **Medium Confidence (50–79%):** Moderate Trust Score or lacking historical/benchmark context. Downstream engines issue directional recommendations with caveats.
* **Low Confidence (< 50%):** Low Trust Score or highly unusual context. Downstream engines pause automated recommendations; flags for human consultant review.

**Example Output:**
> **AI Audit Result:** Operational
> **Confidence:** 82% (High)
> *"Strong internal consistency and artifact-backed evidence support this conclusion."*

---

## SECTION 4: VALIDATION CHECKS

The Validation Layer operates on five core check categories, executed both synchronously (real-time UX) and asynchronously (post-submission).

### 1. Missing Data Detection (Synchronous/Real-time)
* **Definition:** Identifies questions that were skipped or not explicitly marked as "Unknown."
* **Example:** User progresses to the next section without answering Q5.
* **Action:** Triggers a soft UI prompt to complete the field.

### 2. Evidence Quality Detection (Hybrid)
* **Definition:** Evaluates the depth of provided answers against the 5-Level Evidence scale.
* **Example:** User provides a Level 1 one-word answer ("Yes") for a critical governance capability.
* **Action (Sync):** UI nudges for elaboration.
* **Action (Async):** Heavily penalizes the Trust Score if submitted as-is.

### 3. Consistency Validation (Asynchronous/Deep)
* **Definition:** Detects logical contradictions within a single assessment footprint.
* **Example:** User claims "Level 5: Resilient Automation" but later indicates "Daily manual data entry is required."
* **Action:** Flags an internal contradiction; reduces Trust Score.

### 4. Response Depth Validation (Asynchronous/Deep)
* **Definition:** Correlates the strength of a claim with the depth of its explanation.
* **Example:** User claims "Enterprise-wide rollout" but the explanation text is generic and lacks specific tool or owner references.
* **Action:** Modulates the sub-score for that specific capability.

### 5. Benchmark Plausibility Validation (Asynchronous/Deep)
* **Definition:** Compares self-reported maturity against statistical realities for the organization's demographics.
* **Example:** A 10-person startup claims "Scaled Enterprise Governance" typical of a Fortune 500.
* **Action:** Lowers Confidence Index; flags for consultant review.

---

## SECTION 5: VALIDATION SIGNALS

The Validation Layer standardizes signals across all assessment types. In v1, assessments are validated in isolation. Cross-assessment validation (e.g., Leadership vs. Employee) is reserved for the downstream Alignment Engine.

### Assessment Type: Leadership Audit
| Signal Type | Increases Trust | Reduces Trust |
| :--- | :--- | :--- |
| **Evidence Level** | Artifacts provided for strategic initiatives (Level 5) | Assertion only on key governance metrics (Level 1) |
| **Plausibility** | Acknowledges gaps and operational friction | Claims perfect maturity across all APQC domains |
| **Consistency** | Strategic goals align with reported budget allocations | High strategic priority claimed, but zero dedicated resources |

### Assessment Type: Manager Audit
| Signal Type | Increases Trust | Reduces Trust |
| :--- | :--- | :--- |
| **Evidence Level** | Mentions specific SaaS tools and process owners (Level 3-4) | Vague descriptions of team workflows |
| **Consistency** | Reports bottlenecks that align with team size/output | Claims high team efficiency while reporting massive overtime |
| **Response Depth** | Detailed operational narratives in open text | Repeated use of "N/A" for core management capabilities |

### Assessment Type: Employee Audit
| Signal Type | Increases Trust | Reduces Trust |
| :--- | :--- | :--- |
| **Evidence Level** | Specific examples of daily friction or tool usage | Flat, uniform answers down a matrix |
| **Completion** | Explicitly selects "Unknown" for management processes | Skips questions they don't understand |
| **Plausibility** | Responses map logically to their specific department | Answers suggest knowledge outside their scope |

### Assessment Type: AI Audit / Workflow Diagnostic
| Signal Type | Increases Trust | Reduces Trust |
| :--- | :--- | :--- |
| **Evidence Level** | Uploads workflow architecture diagrams | "We use AI for everything" |
| **Consistency** | Security policies match deployed AI tools | Claims high data security but uses public consumer AI tiers |
| **Data State** | Explicitly admits lack of measurement for ROI | Fills in generic, unverifiable ROI numbers |

---

## SECTION 6: SCORING MODEL

The Validation Score operates deterministically. This is a conceptual framework demonstrating the weighting logic, optimizing for verifiable data.

**Validation Score Formula (Conceptual):**

`Trust Score = (Evidence Quality * 0.50) + (Missing Data Penalty * 0.25) + (Internal Consistency * 0.15) + (Response Depth * 0.10)`

**Weighting Logic:**
1. **Evidence Quality (50%):** The heaviest weight. TarkaX prioritizes "how you know" over "what you claim." A Level 5 artifact fundamentally guarantees the reality of the claim, overriding subjective bias.
2. **Missing Data Penalty (25%):** Highly penalizing. Skipped data introduces literal blind spots. (Note: "Lack of Evidence" states do not trigger this penalty).
3. **Internal Consistency (15%):** Captures cognitive dissonance or rushed assessments within a single user session.
4. **Response Depth (10%):** A minor, supporting metric to gauge engagement and effort.

---

## SECTION 7: OUTPUT CONTRACT

The Validation Layer (L2) outputs a structured, machine-readable payload that is passed immutably to the Diagnosis Layer (L3) and Intelligence Layer (L4).

**JSON Output Schema:**

```json
{
  "assessment_id": "uuid",
  "validation_metrics": {
    "trust_score": 81,
    "confidence_index": 76,
    "confidence_tier": "Medium"
  },
  "evidence_profile": {
    "average_evidence_level": 3.2,
    "level_distribution": {
      "level_1": 2,
      "level_2": 5,
      "level_3": 8,
      "level_4": 3,
      "level_5": 2
    },
    "explicit_unknowns_count": 4,
    "missing_data_count": 0
  },
  "flags": {
    "missing_data_flags": [],
    "contradiction_flags": [
      {
        "question_id": "q104",
        "conflict_target": "q112",
        "reason": "Claims high automation (q104) but reports significant manual data entry (q112)."
      }
    ],
    "plausibility_flags": []
  },
  "system_action": "PROCEED_TO_DIAGNOSIS"
}
```

---

## SECTION 8: DOWNSTREAM DEPENDENCIES

The Validation Layer acts as a vital pre-processing step for the core TarkaX engines.

* **Root Cause Engine:** Uses `explicit_unknowns_count` to identify systemic organizational blind spots (e.g., "The root cause of failure is that nobody knows how the process works").
* **Contradiction Engine:** Consumes `contradiction_flags` to begin mapping complex, cross-departmental cognitive dissonance.
* **Alignment Engine:** Uses the `trust_score` to weight conflicting data. If Leadership (Trust: 45) contradicts Employee (Trust: 90), the engine sides with the Employee data.
* **Failure Pattern Engine:** Correlates low `trust_scores` across entire departments to diagnose "Organizational Apathy" or "Change Fatigue."
* **Report V2 (Consultant View):** Displays the `confidence_tier` prominently, framing the entire executive presentation (e.g., "These insights are highly reliable based on rigorous artifact submission").

---

## SECTION 9: IMPLEMENTATION ROADMAP

To prevent overengineering and adhere to controlled convergence, implementation is phased.

### Phase 1 (Current Objective)
* **Focus:** Synchronous UX + Basic Asynchronous Trust Scoring
* **Deliverables:**
  * Implement Missing Data detection (UI prompts).
  * Implement the 5-Level Evidence Quality taxonomy for data collection.
  * Establish explicit "Lack of Evidence" / "Unknown" states in the schema.
  * Calculate base Trust Score (Evidence + Missing Data).
  * Generate `trust_score` payload for downstream use.

### Phase 2 (Fast Follow)
* **Focus:** Deep Asynchronous Validation
* **Deliverables:**
  * Implement Internal Consistency checks (single-assessment logic rules).
  * Implement Response Depth validation logic.
  * Introduce the Confidence Index based on assessment density and historical data.

### Phase 3 (Platform Ecosystem)
* **Focus:** Plausibility & Cross-Audit Foundation
* **Deliverables:**
  * Implement Benchmark Plausibility validation (requires robust historical dataset).
  * Expose Validation Layer outputs directly to the Alignment Engine for cross-assessment weighting.
  * Implement AI-assisted Evidence Level extraction (e.g., auto-verifying Level 5 uploaded artifacts).
