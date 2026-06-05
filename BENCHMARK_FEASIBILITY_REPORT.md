# TarkaX Sprint 5C.1 — Benchmark Data Feasibility Report

## Executive Summary

**Can benchmarking be built today?**
**Answer: Partially**

Based on a structural audit of the current TarkaX system schema (database models, APIs, and payloads), the platform is currently equipped to calculate **Platform Average Benchmarks** (Overall and Dimension-level averages). However, more granular benchmarking (Industry, Company Size, Geography, etc.) is structurally impossible today because the required metadata is not collected from organizations or users.

---

## Data Inventory

The following benchmark inputs are **Structurally Supported** by the current schema (specifically within the `Audit` model):

| Metric | Status | Evidence |
| :--- | :--- | :--- |
| **Total Score** | Structurally Supported | `Audit.total_score` (Integer, Nullable) |
| **Awareness Score** | Structurally Supported | Nested in `Audit.scores` JSON field |
| **Adoption Score** | Structurally Supported | Nested in `Audit.scores` JSON field |
| **Integration Score** | Structurally Supported | Nested in `Audit.scores` JSON field |
| **Governance Score** | Structurally Supported | Nested in `Audit.scores` JSON field |
| **ROI Score** | Structurally Supported | Nested in `Audit.scores` JSON field |

*Note: Current assessment volume cannot be verified from the available repository and local environment. Benchmark feasibility is therefore evaluated based purely on the system's structural ability to collect and organize benchmark data.*

---

## Missing Data

The following required benchmark inputs are currently not collected. They do not exist on the `Audit`, `Organization`, or `User` models:

| Metadata | Present? | Evidence |
| :--- | :--- | :--- |
| **Industry** | Missing | `industry` field absent from schema |
| **Company Size** | Missing | `company_size` / `employee_count` absent from schema |
| **Geography** | Missing | `geography` / `location` absent from schema |
| **Department** | Missing | `department` absent from schema |
| **Organization Type** | Missing | `organization_type` absent from schema |
| **Revenue Band** | Missing | `revenue` absent from schema |

*Exception Note: While a `workflows` table contains an `input_config` JSON which might specify an `industry_variant` internally for blueprints, this is not systematically captured at the organizational or audit level for standardized comparison.*

---

## Feasibility Matrix

| Benchmark Type | Feasible | Confidence |
| :--- | :--- | :--- |
| **Platform Average** | Yes | 100% (Structurally possible to compute aggregations of total scores and dimension scores across all audits) |
| **Industry** | No | 0% (Required metadata `industry` is structurally missing) |
| **Company Size** | No | 0% (Required metadata `company_size` is structurally missing) |
| **Geography** | No | 0% (Required metadata `geography` is structurally missing) |

---

## Data Consistency and Trust Risks

**1. Data Consistency Issues**
Since fields like `total_score` and `scores` are configured as nullable in the schema (`Mapped[int | None] = mapped_column(Integer, nullable=True)`), partial or abandoned audits might result in missing data. Therefore, any benchmark calculations must strictly filter out incomplete assessments (`status != 'complete'`) and handle null scores robustly to maintain data integrity.

**2. Trust Risks Identified**
*   **Industry/Region Benchmarks without data:** It is misleading to display "Industry Comparisons" when we do not collect explicit industry definitions.
*   **Small Sample Sizes:** Displaying percentiles or averages when the total platform volume is very small compromises the credibility of the platform.

---

## Minimum Sample Analysis

To preserve product credibility and trust, benchmarking must not be displayed if the sample size is statistically meaningless.

**Recommended guidance:**
* **<10** → No benchmark shown (Refuse to generate claims)
* **10–25** → Low confidence
* **25–50** → Moderate confidence
* **50+** → Strong confidence

**Recommendation:** Set the minimum benchmark threshold to **10**. The system should outright refuse to generate or display benchmark comparisons for any grouping that has fewer than 10 completed, valid assessments.

---

## Recommended Next Step

**C. Build platform-average benchmarking only**

*Rationale:* Proceeding to Sprint 5C.2 is viable, but the scope must be strictly limited to Platform Average comparisons. Expanding to other benchmark types (Industry, Company Size, etc.) would require a prerequisite schema migration and user data collection effort, which contradicts the immediate objective of relying on what is possible *today*.
