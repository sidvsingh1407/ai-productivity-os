# TARKAX Workflow Diagnostic Framework

**Version:** 1.0.0
**Status:** ACTIVE
**Description:** A reusable, workflow-agnostic diagnostic framework to evaluate operational workflows across any business function.

---

## PART 1 & 3: DIAGNOSTIC DIMENSIONS & QUESTION BANK

This framework evaluates workflows across 10 standardized dimensions.
Two additional dimensions (Tool Sprawl / Integration Friction, and Resilience / Exception Handling) have been proactively added to enhance operational intelligence and systems architecture depth.

### Bottlenecks

**Definition:** The degree to which work items accumulate at specific stages due to capacity constraints, approval requirements, or resource starvation.

**Why it matters:** Bottlenecks dictate the maximum throughput of the entire system. Optimizing non-bottleneck steps yields zero systemic improvement.

**Signals:**
- High queue times
- Resource utilization approaching 100% at specific nodes
- Frequent escalations to expedite work

**Metrics:**
- Queue Wait Time
- WIP (Work In Progress) to Completion Ratio
- Approval Turnaround Time

**Example Indicators:**
- Approvals pending for > 48 hours
- Single individual responsible for 80% of step execution

**Failure Patterns:**
- The 'Hero' Anti-Pattern (one person does everything)
- Batch Processing Delays (waiting for end of week/month)

#### Diagnostic Questions (Answer Scale: A-E)
bot_01. What percentage of workflow steps require human approval before proceeding?
bot_02. How often do tasks sit idle waiting for a specific resource or role to become available?
bot_03. Is there a single step where work consistently accumulates faster than it can be processed?
bot_04. How frequently are SLA (Service Level Agreement) deadlines missed due to wait times at a specific stage?
bot_05. When the volume of work increases by 20%, does the processing time increase exponentially rather than linearly?
bot_06. How often are 'expedite' or 'rush' requests used to bypass standard queues?
bot_07. Are there specific individuals whose absence (e.g., vacation, illness) brings the workflow to a halt?
bot_08. What is the ratio of active processing time to idle wait time for a typical work item?
bot_09. How often does batching (e.g., waiting for end-of-day processing) cause downstream delays?
bot_10. Are queues visible to all participants, or are bottlenecks only discovered after deadlines pass?

---

### Governance

**Definition:** The structural oversight, policy adherence, and standardized operational procedures that regulate how the workflow is executed.

**Why it matters:** Without governance, workflows degrade into ad-hoc processes, increasing operational risk, inconsistency, and audit failures.

**Signals:**
- Inconsistent outputs
- Lack of clear ownership
- Frequent policy violations

**Metrics:**
- Standard Operating Procedure (SOP) Adherence Rate
- Audit Finding Frequency
- Policy Exception Rate

**Example Indicators:**
- No documented SOPs exist
- Decisions are made via untracked Slack/Teams messages

**Failure Patterns:**
- Shadow IT/Processes
- Orphaned Workflows (no clear owner)

#### Diagnostic Questions (Answer Scale: A-E)
gov_01. Is there a clearly documented, up-to-date Standard Operating Procedure (SOP) for this workflow?
gov_02. Is there a designated single point of accountability (owner) for the end-to-end workflow?
gov_03. How frequently are exceptions to standard policy requested and granted?
gov_04. Are all workflow modifications or updates formally reviewed and approved before implementation?
gov_05. How often are steps executed differently depending on which individual is assigned?
gov_06. Is there a defined escalation matrix for when edge cases or disputes occur?
gov_07. Are historical records of workflow execution maintained and easily accessible for audit purposes?
gov_08. Do participants receive formal training and certification before executing critical workflow steps?
gov_09. Are the operational limits and authority thresholds explicitly defined for all roles?
gov_10. How often is the workflow periodically reviewed for alignment with current business objectives?

---

### Automation

**Definition:** The extent to which programmatic systems execute workflow steps without human intervention.

**Why it matters:** Automation drives scalability, reduces human error, and lowers per-transaction operational costs.

**Signals:**
- High volume of manual data entry
- Copy-pasting between systems
- Repetitive deterministic tasks

**Metrics:**
- Percentage of Automated Steps
- Manual Intervention Rate
- Straight-Through Processing (STP) Rate

**Example Indicators:**
- Staff spend >2 hours daily manually syncing data
- Triggers are manual rather than event-driven

**Failure Patterns:**
- Swivel-Chair Integration (human as the API)
- Brittle Scripts (unmaintained macros)

#### Diagnostic Questions (Answer Scale: A-E)
aut_01. What percentage of the workflow's data entry involves manual typing or copy-pasting between systems?
aut_02. Are workflow triggers event-driven (e.g., system alert) or manual (e.g., someone sending an email)?
aut_03. How often do humans perform deterministic tasks that follow rigid IF/THEN rules without requiring judgment?
aut_04. Is data automatically validated upon entry, or does it require manual review for correctness?
aut_05. What is the Straight-Through Processing (STP) rate where a task completes with zero human touch?
aut_06. Are status updates and notifications generated automatically by the system?
aut_07. How reliant is the workflow on unmanaged local macros or personal spreadsheets?
aut_08. Do systems autonomously retrieve necessary enrichment data, or must humans search for it?
aut_09. How frequently do automated steps fail, requiring manual fallback procedures?
aut_10. Are documents (e.g., invoices, reports) automatically generated from structured data?

---

### Visibility

**Definition:** The degree of transparency into the real-time status, historical performance, and operational state of the workflow.

**Why it matters:** Without visibility, management operates blindly, making it impossible to proactively address issues or optimize performance.

**Signals:**
- Inability to locate work items
- Manual status reporting
- Surprise failures

**Metrics:**
- Time to Retrieve Status
- Dashboard Coverage Ratio
- Data Latency

**Example Indicators:**
- Status meetings are required just to know where things stand
- Tracking relies on a static Excel file updated weekly

**Failure Patterns:**
- Black Box Operations
- Stale Data Reporting

#### Diagnostic Questions (Answer Scale: A-E)
vis_01. Can stakeholders view the real-time status of any active item without asking a human?
vis_02. Are key performance metrics (KPIs) available via a live, automated dashboard?
vis_03. How much time is spent weekly manually compiling status reports for management?
vis_04. Is there a clear, auditable trail showing exactly who did what, and when?
vis_05. When an item is delayed, are automatic alerts triggered, or is it only noticed reactively?
vis_06. Are performance trends (e.g., throughput over the last 30 days) easily accessible?
vis_07. Can you immediately identify where an item is stuck and who is responsible for the next step?
vis_08. Is the underlying data source for reporting a single source of truth (SSOT)?
vis_09. How often do different teams report conflicting numbers regarding the same workflow?
vis_10. Are workflow participants aware of their own performance metrics relative to targets?

---

### Handoff Quality

**Definition:** The reliability, completeness, and clarity of information transferred between distinct steps, systems, or teams.

**Why it matters:** Friction at system and human boundaries causes rework, delays, and context loss, severely degrading workflow efficiency.

**Signals:**
- High rework rates
- Missing context at handoff
- Ping-ponging of tasks back and forth

**Metrics:**
- Rework / Rejection Rate
- Information Completeness Score
- Handoff Delay Time

**Example Indicators:**
- Tasks are frequently returned because 'missing information'
- Downstream teams have to manually verify upstream data

**Failure Patterns:**
- Garbage In, Garbage Out (GIGO)
- The 'Over-the-Wall' Toss

#### Diagnostic Questions (Answer Scale: A-E)
han_01. How frequently are tasks rejected or sent back upstream due to missing or incorrect information?
han_02. Is there a strict validation gate ensuring all required data is present before a handoff occurs?
han_03. When work is handed off, is the full context transferred, or do assignees have to ask for clarification?
han_04. Are handoffs standardized via structured forms/APIs, or are they unstructured (e.g., email text)?
han_05. How often do downstream systems/teams need to manually reformat data received from upstream?
han_06. Is it clear exactly when responsibility shifts from one party to another?
han_07. Do cross-functional teams share a common vocabulary for the data being transferred?
han_08. How much time elapses between a task being 'completed' by team A and 'started' by team B?
han_09. Are handoff failures automatically logged and tracked for root cause analysis?
han_10. Is there a Service Level Agreement (SLA) governing the quality and speed of handoffs?

---

### Knowledge Dependency

**Definition:** The reliance on tacit, undocumented human knowledge or specialized expertise to execute workflow steps.

**Why it matters:** High knowledge dependency creates massive operational risk, limiting scale and making the workflow vulnerable to employee turnover.

**Signals:**
- Only one person knows how to do it
- Long onboarding times
- Tribal knowledge overrides documentation

**Metrics:**
- Time to Competency (for new hires)
- Bus Factor
- Documentation Coverage

**Example Indicators:**
- 'Ask Sarah, she's the only one who knows how this works'
- New hires take 6 months to become productive

**Failure Patterns:**
- Key Person Risk
- Undocumented Edge Cases

#### Diagnostic Questions (Answer Scale: A-E)
kno_01. How long does it take for a new team member to become fully productive in this workflow?
kno_02. Are the decision-making rules explicitly documented, or do they rely on 'gut feeling' and experience?
kno_03. If the primary operator were to leave unexpectedly, could the workflow continue without severe disruption?
kno_04. How often do undocumented 'workarounds' need to be used to successfully complete tasks?
kno_05. Is the documentation detailed enough that an adjacent team member could execute the steps accurately?
kno_06. How frequently is tacit 'tribal knowledge' required to resolve edge cases?
kno_07. Are training materials systematically updated when the process changes?
kno_08. Is knowledge centralized in a searchable base, or dispersed across personal notes and emails?
kno_09. Do complex steps feature contextual guidance (e.g., tooltips, inline help) directly in the tools used?
kno_10. What is the 'Bus Factor' (number of people who must be incapacitated to halt the workflow)?

---

### Compliance

**Definition:** The ability of the workflow to consistently adhere to internal policies, external regulations, and security standards.

**Why it matters:** Non-compliance results in regulatory fines, legal liability, reputational damage, and loss of business operating licenses.

**Signals:**
- Skipped security checks
- Unapproved access
- Failed audits

**Metrics:**
- Control Failure Rate
- Audit finding severity
- Data Exposure Incidents

**Example Indicators:**
- Sensitive data sent via unsecured email
- Steps mandating dual-authorization are bypassed

**Failure Patterns:**
- Security as an Afterthought
- Rubber-Stamping Approvals

#### Diagnostic Questions (Answer Scale: A-E)
com_01. Does the workflow natively enforce mandatory regulatory or security checks without human intervention?
com_02. Is all sensitive data (PII, PHI, financial) handled in accordance with strict security standards?
com_03. Are complete, immutable audit logs generated for all critical actions and data state changes?
com_04. How often do operators bypass compliance steps to meet deadlines or throughput goals?
com_05. Is access to the workflow tools strictly governed by the Principle of Least Privilege?
com_06. Are compliance requirements updated automatically when external regulations change?
com_07. Has the workflow ever failed an internal or external compliance audit?
com_08. Are approvals cryptographically or systematically verified to prevent 'rubber-stamping'?
com_09. Is data retention and deletion handled according to predefined compliance schedules?
com_10. Do compliance controls introduce significant friction, or are they seamlessly integrated?

---

### Throughput

**Definition:** The volume of work successfully completed by the workflow over a specific period, relative to its maximum capacity.

**Why it matters:** Throughput measures the actual productivity and economic output of the workflow. Low throughput indicates high friction or inefficiency.

**Signals:**
- Backlogs growing faster than completion
- High cycle times
- Low output per FTE

**Metrics:**
- Cycle Time
- Items Completed per Hour/Day
- Capacity Utilization Rate

**Example Indicators:**
- It takes 14 days to process a request that requires 2 hours of actual work
- The queue is permanently growing

**Failure Patterns:**
- Starved Resources
- Excessive Context Switching

#### Diagnostic Questions (Answer Scale: A-E)
thr_01. What is the average Cycle Time from the initiation of a request to its final completion?
thr_02. Is the current output volume sufficient to meet business demands without accruing a backlog?
thr_03. How stable is the throughput day-over-day (is it consistent, or highly volatile)?
thr_04. Does the system experience frequent periods of 'starvation' where resources have no work to do?
thr_05. How much does context switching (handling multiple different types of tasks) degrade overall output?
thr_06. Is the throughput constrained by system performance (e.g., slow software loading times)?
thr_07. Can throughput be predictably scaled by adding resources linearly?
thr_08. What percentage of work requires rework, effectively reducing net successful throughput?
thr_09. Are there specific periods (e.g., end of month) where throughput dramatically drops due to congestion?
thr_10. How does the actual throughput compare to the theoretical maximum capacity of the workflow?

---

### Tool Sprawl / Integration Friction

**Definition:** The degree to which a workflow requires context switching across multiple disconnected applications, leading to operational fragmentation.

**Why it matters:** Excessive tooling increases licensing costs, cognitive load, data duplication, and the probability of systemic errors.

**Signals:**
- Multiple open tabs to do one job
- Data inconsistencies between systems
- User fatigue

**Metrics:**
- Applications Touched per Workflow
- API Error Rate
- Time Spent Context Switching

**Example Indicators:**
- Operators must log into 5 different portals to complete one customer request
- Data is manually synced between a CRM and an ERP

**Failure Patterns:**
- Frankenstein Architecture
- SaaS Fatigue

#### Diagnostic Questions (Answer Scale: A-E)
tsp_01. How many distinct software applications must a user interact with to complete this workflow?
tsp_02. How often must users manually transfer data from one system to another?
tsp_03. Is there a single source of truth for the data, or are there conflicting records across systems?
tsp_04. How frequently do API integrations between these tools fail or silently drop data?
tsp_05. Does navigating between different tool interfaces cause significant cognitive load or delays?
tsp_06. Are users creating shadow IT solutions (e.g., personal databases) to bypass cumbersome tools?
tsp_07. How often is data out of sync across the different platforms used in the workflow?
tsp_08. Is the tooling architecture intentionally designed, or did it evolve ad-hoc over time?
tsp_09. Do users require multiple different credentials to access necessary systems?
tsp_10. How difficult is it to onboard a new user to all the necessary tools for this workflow?

---

### Resilience / Exception Handling

**Definition:** The capacity of the workflow to gracefully detect, manage, and recover from errors, edge cases, and systemic failures.

**Why it matters:** Fragile workflows crash completely when encountering unexpected inputs, causing massive disruptions and requiring expensive manual triage.

**Signals:**
- Unmanaged exceptions
- System crashes requiring IT support
- Lost data during outages

**Metrics:**
- Mean Time to Recovery (MTTR)
- Exception Rate
- Automated Recovery Success Rate

**Example Indicators:**
- A single malformed email attachment stops the entire processing pipeline
- No clear protocol exists when the primary database is down

**Failure Patterns:**
- Happy Path Only Design
- Silent Failures

#### Diagnostic Questions (Answer Scale: A-E)
res_01. When an unexpected input or error occurs, does the workflow fail gracefully or crash entirely?
res_02. Is there a dedicated, standardized process for managing and resolving exceptions?
res_03. Are errors systematically logged and routed to the appropriate team for rapid triage?
res_04. Can the workflow automatically retry transient failures (e.g., temporary network timeouts)?
res_05. How long does it typically take to identify and resolve a system-level failure affecting the workflow?
res_06. If a downstream system goes offline, is data safely queued or permanently lost?
res_07. Are 'unhappy paths' (edge cases) explicitly designed and tested, or largely ignored?
res_08. Does the system provide clear, actionable error messages to users rather than technical stack traces?
res_09. Is there a fallback manual procedure available when critical systems are unavailable?
res_10. How frequently do the same types of exceptions recur without underlying root cause resolution?

---

## PART 2: SCORING SYSTEM

The framework employs a 0-100 quantitative scoring model designed to be deterministic and machine-readable.

### Core Scores
- **Dimension Score (0-100):** Calculated per dimension based on responses.
- **Workflow Health Score (0-100):** Weighted average of all 10 Dimension Scores.
- **Confidence Score (0-100):** Reflects data reliability, completeness, and evidence backing.

### Answer Scale Mapping
- **A (100):** Optimized / Always
- **B (75):** Healthy / Mostly
- **C (50):** Developing / Sometimes
- **D (25):** Weak / Rarely
- **E (0):** Critical / Never

### Risk Classification & Status
Derived from the Workflow Health Score, maintaining TARKAX governance compatibility:

| Range | Classification | Risk Status |
|-------|----------------|-------------|
| 81-100| Optimized      | Healthy     |
| 61-80 | Healthy        | Healthy     |
| 41-60 | Developing     | Watch       |
| 21-40 | Weak           | Risk        |
| 0-20  | Critical       | Critical    |

### Normalization & Weighting
- **Default:** Equal weighting (10% per dimension).
- **Dynamic Normalization:** Weights can be adjusted based on workflow class (e.g., Compliance weighted 20% in Finance, Throughput weighted 20% in Operations).

---

## PART 4: RECOMMENDATION ENGINE

For programmatic remediation, each dimension maps to deterministic root causes and actionable suggestions.

### Bottlenecks
**Common Root Causes:**
- Single point of failure
- Overly strict authorization policies
- Resource under-allocation
**Remediation Suggestions:**
- Implement parallel processing where sequential steps are not strictly required
- Introduce auto-approval thresholds for low-risk items
- Cross-train staff to alleviate single-resource dependency

### Governance
**Common Root Causes:**
- Lack of documentation
- Unclear role definitions
- Decentralized decision-making
**Remediation Suggestions:**
- Establish a formal RACI matrix
- Digitize and version-control SOPs
- Implement enforced decision gates with audit logging

### Automation
**Common Root Causes:**
- Legacy systems lacking APIs
- Under-investment in tooling
- Process not standardized enough to automate
**Remediation Suggestions:**
- Deploy RPA for legacy UI interactions
- Implement API-driven data synchronization
- Standardize unstructured inputs into structured web forms

### Visibility
**Common Root Causes:**
- Siloed systems
- Lack of central tracking database
- Manual reporting culture
**Remediation Suggestions:**
- Implement a unified operational dashboard
- Enforce state-change logging in the core system of record
- Replace status meetings with automated alert subscriptions

### Handoff Quality
**Common Root Causes:**
- Lack of required field validation
- Misaligned team incentives
- Incompatible data formats
**Remediation Suggestions:**
- Implement strict entry/exit criteria for workflow stages
- Use structured intake forms with mandatory fields
- Standardize data schemas across boundaries

### Knowledge Dependency
**Common Root Causes:**
- Complex legacy processes
- Lack of documentation culture
- High turnover environments
**Remediation Suggestions:**
- Extract tacit knowledge into decision matrices
- Implement inline contextual help in applications
- Force job rotations to build cross-training

### Compliance
**Common Root Causes:**
- Controls disconnected from actual work
- Lack of automated enforcement
- Poorly defined regulatory requirements
**Remediation Suggestions:**
- Shift compliance controls 'left' (earlier in the process)
- Implement immutable audit trails
- Automate data masking and access controls

### Throughput
**Common Root Causes:**
- Unmanaged backlogs
- High rework rates
- System latency
**Remediation Suggestions:**
- Implement WIP limits to focus on completion
- Optimize database/system response times
- Standardize task batching to reduce context switching

### Tool Sprawl / Integration Friction
**Common Root Causes:**
- Lack of central enterprise architecture
- Siloed purchasing decisions
- Inadequate APIs
**Remediation Suggestions:**
- Consolidate overlapping SaaS tools
- Implement an Enterprise Service Bus or iPaaS (e.g., Zapier/MuleSoft) for API sync
- Build unified frontend interfaces masking complex backends

### Resilience / Exception Handling
**Common Root Causes:**
- Lack of error boundaries
- Optimistic assumptions about data quality
- Inadequate monitoring
**Remediation Suggestions:**
- Implement Dead Letter Queues (DLQs) for failed transactions
- Design explicit fallback routing for edge cases
- Enhance telemetry and alerting for failure states

---

## PART 5: WORKFLOW HEALTH REPORT

The final output is structured to serve executive, operational, and technical stakeholders.

### Report Structure
1. **Executive Summary:** High-level overview, primary constraint identified.
2. **Workflow Health Score:** 0-100 score with Risk Status (e.g., '65 - Healthy').
3. **Dimension Scores:** Radar chart representation of all 10 dimensions.
4. **Bottleneck Analysis:** Specific queues and constraints identified.
5. **Governance Analysis:** SOP and policy adherence breakdown.
6. **Risk Analysis:** Compliance and Exception handling vulnerabilities.
7. **Recommendations:** AI-generated remediation tactics.
8. **Priority Actions:** The top 3 immediate fixes for highest ROI.
9. **Maturity Assessment:** Long-term evolution roadmap.

### Example Output Snippet
```
WORKFLOW: Customer Onboarding (Sales -> CS)
HEALTH SCORE: 42 (Developing)
RISK STATUS: Watch

CRITICAL FINDINGS:
- Handoff Quality: 20 (Critical) - Frequent missing CRM data causes 48h delays.
- Tool Sprawl: 35 (Weak) - Team uses 4 disconnected apps to provision accounts.

PRIORITY ACTION:
Implement mandatory structured intake form (Zod validation) at Sales handoff gate to eliminate downstream data missing errors.
```

---

## PART 6: APQC MAPPING & CROSS-FUNCTIONAL APPLICATION

The framework evaluates the *meta-properties* of workflow execution, making it universally applicable across APQC categories:

- **HR (Onboarding):** Identifies *Bottlenecks* (waiting for IT) and *Handoff Quality* (HR to Manager).
- **Finance (Procure-to-Pay):** Evaluates *Compliance* (fraud checks) and *Automation* (invoice parsing).
- **Sales (Quote-to-Cash):** Highlights *Visibility* (deal tracking) and *Tool Sprawl* (CRM to CPQ friction).
- **Marketing (Campaign Launch):** Assesses *Governance* (brand approvals) and *Throughput* (assets produced).
- **IT (Incident Management):** Diagnoses *Resilience* (MTTR) and *Knowledge Dependency* (reliance on L3 heroes).

---

## PART 7: FUTURE AI EXTENSIONS

The JSON artifact of this framework is designed to connect to the broader TARKAX intelligence ecosystem.

### Recommendation Engine
- **Inputs:** Dimension Scores, Failure Patterns
- **Outputs:** Actionable Remediation Steps, ROI Estimates
- **Integration Point:** Post-diagnostic scoring phase.

### Benchmarking Engine
- **Inputs:** Workflow Health Score, Industry Tag, APQC Category
- **Outputs:** Percentile Ranking, Peer Comparisons
- **Integration Point:** Data warehouse analytics layer.

### TimesFM Forecasting
- **Inputs:** Historical Throughput Data, Queue Wait Times
- **Outputs:** Predicted SLA Violations, Capacity Shortfall Alerts
- **Integration Point:** Real-time workflow monitoring feeds.

### Simulation Engine
- **Inputs:** Process Graph, Bottleneck Metrics
- **Outputs:** What-If Scenario Analysis (e.g., Impact of adding 2 FTEs)
- **Integration Point:** Digital Twin modeling environment.

### MiroFish Diagram Extraction
- **Inputs:** Unstructured BPMN Diagrams, Visio Files
- **Outputs:** Structured JSON Process Ontology, Initial Diagnostic Pre-fill
- **Integration Point:** Ingestion and onboarding pipeline.

---

## PART 8: PM REVIEW

1. **Is this framework scalable to hundreds of workflows?**
   Yes. It utilizes a deterministic, rule-based JSON schema that allows programmatic execution via APIs or LLM pipelines across massive workflow datasets.

2. **Does it remain workflow-agnostic?**
   Yes. By analyzing meta-properties (throughput, friction, visibility) rather than domain specifics, it applies identically to IT and Finance.

3. **Does it align with APQC process structures?**
   Yes. It acts as an evaluation layer that sits on top of standard APQC Process Classification Frameworks, assessing the 'health' of the processes mapped within the APQC structure.

4. **What are the biggest weaknesses?**
   Subjectivity in survey responses (if humans answer the questions manually) and the baseline assumption that all dimensions carry equal weight, which may skew results if not dynamically adjusted per industry.

5. **What should be improved before implementation?**
   Establish exact API schemas for how diagnostic data is automatically ingested (e.g., directly parsing Jira/Salesforce logs) to transition from manual Q&A to real-time programmatic telemetry.
