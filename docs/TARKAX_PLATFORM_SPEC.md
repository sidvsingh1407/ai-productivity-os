# TARKAX Platform Specification

> **Document Status:** PRE-PLATFORM STANDARDIZATION
> **Purpose:** Constitutional document for future platform evolution and controlled convergence.
> **Audience:** Future engineering team, product managers, platform architects, and key stakeholders.

---

## 0. PLATFORM READINESS ASSESSMENT

Before defining the future state, we must evaluate our current operational readiness for platform convergence.

### Assessment Scores

| Domain | Current State | Gaps | Readiness Level |
|---|---|---|---|
| **AI Productivity OS** | Activation path functional; audit engine operational. | Frontend stabilization ongoing; missing core platform analytics. | **Medium** |
| **AWDE** | Independent product in stabilization phase. | Lacks shared domain models with OS; isolated workflow execution. | **Low** |
| **Shared Identity** | Defined user models (`User`), roles, and JWT auth. | Missing cross-product SSO and unified session management. | **Medium** |
| **Shared Data Models** | Core shared tables exist (`Organization`, `User`). | Product-specific tables (`Blueprint`, `Audit`) lack canonical platform abstraction. | **Low** |
| **Shared Events** | Non-existent. Products run isolated logic. | No event bus, no standardized event schemas. | **None** |
| **Shared Analytics** | None. | No telemetry or centralized usage data. | **None** |
| **Shared Governance** | Basic organizational separation. | Missing comprehensive RBAC, compliance logging, and audit trails. | **Low** |

---

## 1. PLATFORM VISION

### What TARKAX Is
TARKAX is a unified operational intelligence platform. It provides a cohesive ecosystem for evaluating, diagnosing, and optimizing business operations through structural analysis and rule-based diagnostic engines.

### What TARKAX Is NOT
TARKAX is **not** an orchestration engine, a workflow builder (like Zapier or Make), an execution runtime, or a generic task management tool. It does not replace operational systems of record.

### Long-Term Positioning
TARKAX will position itself as the "Diagnostic Layer" for enterprise operations—a suite of specialized, interoperable tools unified by a single identity, governance model, and data taxonomy.

### Platform Philosophy: Controlled Convergence
We reject premature platformization. Independent products will stabilize individually before migrating shared responsibilities down to the platform infrastructure level. We will build platform capabilities strictly when two or more stabilized products require the exact same infrastructure.

---

## 2. PRODUCT BOUNDARIES

To prevent "big ball of mud" architecture, we must strictly delineate product logic from platform infrastructure.

### AI Productivity OS
**Responsibilities:** AI maturity audits, organizational assessments, governance scoring, compliance insights, productivity intelligence.
**Scope:** Strictly handles the evaluation of high-level organizational readiness and maturity.

### AWDE (Workflow Diagnostic)
**Responsibilities:** Deterministic workflow diagnostics, structural bottleneck detection, ambiguity analysis, governance-aware workflow scoring.
**Scope:** Strictly handles the evaluation of specific, individual workflows and processes.

### Future Products (Placeholders)
Future products (e.g., Reporting Intelligence, Audit Intelligence) will plug into the platform shell and operate on the shared domain model without interfering with existing product execution.

### Platform Infrastructure vs. Product Logic
*   **Belongs in Infrastructure:** Identity, routing, workspace context, billing, unified telemetry, core data entities (User, Org).
*   **Belongs in Product:** Scoring engines, diagnostic rulesets, product-specific forms, specialized reporting logic, specific UI visualizers.

---

## 3. SHARED PLATFORM CAPABILITIES

As we converge, these capabilities will move from product silos to shared infrastructure.

| Capability | Purpose | Ownership | Future Timing |
|---|---|---|---|
| **Authentication & SSO** | Centralized login and session management across all TARKAX products. | Platform Core | Phase 1 |
| **Authorization (RBAC)** | Standardized roles and permissions enforced at the API gateway. | Platform Core | Phase 1 |
| **Organization & User Management** | Unified management of members, teams, and invites. | Platform Core | Phase 1 |
| **Analytics & Telemetry** | Centralized tracking of feature usage and system performance. | Platform Data | Phase 3 |
| **Observability** | Unified logging and error tracking. | Platform Infra | Phase 2 |
| **Notifications** | Centralized engine for email and in-app alerts. | Platform Core | Phase 3 |
| **Billing & Subscriptions** | Consolidated invoicing and tier management per organization. | Platform Finance | Phase 3 |
| **Reporting Core** | Shared libraries for PDF/CSV generation and data exports. | Platform Core | Phase 4 |
| **Audit Trail** | Immutable ledger of all significant platform actions. | Platform Security | Phase 2 |

---

## 4. SHARED DOMAIN MODEL

The following canonical entities form the foundation of the TARKAX platform.

### Core Entities

*   **User**
    *   *Purpose:* Represents a human interacting with the platform.
    *   *Ownership:* Platform Core
    *   *Key Fields:* `id`, `email`, `full_name`, `is_superadmin`, `is_active`
    *   *Relationships:* Belongs to Organizations via `OrgMember`.
*   **Organization**
    *   *Purpose:* The primary tenant isolation boundary.
    *   *Ownership:* Platform Core
    *   *Key Fields:* `id`, `name`, `slug`
    *   *Relationships:* Contains `OrgMember`, owns `Audits`, `Workflows`, `Subscriptions`.
*   **Workspace / Project** (Future Abstraction)
    *   *Purpose:* Logical grouping of related audits and workflows within an organization.
    *   *Ownership:* Platform Core
    *   *Relationships:* Belongs to `Organization`, contains product entities.
*   **Audit**
    *   *Purpose:* A structured organizational assessment.
    *   *Ownership:* AI Productivity OS
    *   *Key Fields:* `id`, `status`, `scores`, `total_score`, `form_response`
    *   *Relationships:* Belongs to `Organization` and `User`.
*   **Workflow**
    *   *Purpose:* A deterministic operational map submitted for structural diagnosis.
    *   *Ownership:* AWDE
    *   *Key Fields:* `id`, `status`, `input_config`
    *   *Relationships:* Belongs to `Organization` and `User`, contains `Blueprints`.
*   **Report**
    *   *Purpose:* A generated artifact (e.g., PDF/CSV) representing analysis outcomes.
    *   *Ownership:* Platform Core
    *   *Key Fields:* `id`, `file_path`, `generated_at`
*   **Subscription**
    *   *Purpose:* Represents the active billing tier for a tenant.
    *   *Ownership:* Platform Finance
    *   *Key Fields:* `id`, `status`, `plan_id`
    *   *Relationships:* Unique to an `Organization`.
*   **Event / Notification / AuditLog**
    *   *Purpose:* Platform-wide activity markers and messaging units.
    *   *Ownership:* Platform Core

---

## 5. SHARED EVENT CONTRACTS

When products need to communicate or trigger shared capabilities, they will use standardized events.

**`USER_CREATED`**
```json
{
  "event": "USER_CREATED",
  "user_id": "uuid",
  "email": "user@example.com",
  "timestamp": "2024-06-01T12:00:00Z"
}
```
*   *Producer:* Auth Service
*   *Consumers:* Analytics, Billing, Notification Service

**`USER_LOGGED_IN`**
```json
{
  "event": "USER_LOGGED_IN",
  "user_id": "uuid",
  "ip_address": "192.168.1.1",
  "timestamp": "2024-06-01T12:00:00Z"
}
```
*   *Producer:* Auth Service
*   *Consumers:* Security Logging, Analytics

**`AUDIT_COMPLETED`**
```json
{
  "event": "AUDIT_COMPLETED",
  "audit_id": "uuid",
  "org_id": "uuid",
  "user_id": "uuid",
  "total_score": 85,
  "timestamp": "2024-06-01T12:00:00Z"
}
```
*   *Producer:* AI Productivity OS Engine
*   *Consumers:* Billing (metering), Reporting Engine, Webhook dispatcher

**`WORKFLOW_DIAGNOSED`** (Analog to WORKFLOW_COMPLETED)
```json
{
  "event": "WORKFLOW_DIAGNOSED",
  "workflow_id": "uuid",
  "org_id": "uuid",
  "health_score": 72,
  "timestamp": "2024-06-01T12:00:00Z"
}
```
*   *Producer:* AWDE Engine
*   *Consumers:* Billing, Reporting Engine

**`REPORT_GENERATED`**
```json
{
  "event": "REPORT_GENERATED",
  "report_id": "uuid",
  "source_entity_id": "uuid",
  "source_type": "audit|workflow",
  "download_url": "https://...",
  "timestamp": "2024-06-01T12:00:00Z"
}
```
*   *Producer:* Reporting Service
*   *Consumers:* Notification Service (email delivery)

---

## 6. OBSERVABILITY STANDARD

We define the standard for future platform operations. *(Do not implement yet; specification only).*

*   **Logging Standards:** All services must output structured JSON logs to `stdout`. Logs must include `trace_id`, `org_id`, and `user_id` when in context.
*   **Telemetry Standards:** System metrics (CPU, Memory, Request Latency) must be exposed via standard endpoints (e.g., Prometheus format) to be scraped by infrastructure monitors.
*   **Audit Trail Standards:** Any mutation to a core entity (User, Org, Permissions) must generate an immutable log entry containing the actor, action, timestamp, and pre/post state changes.
*   **Operational Metrics:** Business metrics (e.g., "Time to complete audit form", "Average workflow diagnostic score") must be tracked independently from system telemetry.

---

## 7. SECURITY & GOVERNANCE MODEL

*   **RBAC Model:** We will implement standard roles: `Org Owner`, `Org Admin`, `Org Member`, `Read-Only`.
*   **Organization Isolation:** Data must be strictly isolated by `org_id`. Cross-tenant data access is strictly prohibited at the database query level.
*   **Audit Requirements:** Significant destructive actions (e.g., deleting an organization) require a secondary confirmation and log entry.
*   **Compliance Considerations:** Data structures must support GDPR (right to be forgotten) and SOC2 (access logging).
*   **Permission Inheritance:** Permissions are granted at the Organization level and inherited downward to Workspaces/Projects and specific resources.

---

## 8. PLATFORM SHELL SPECIFICATION

The "Platform Shell" is the unified UI container. Products are plugins inside this shell. The shell itself contains *zero* product-specific diagnostic logic.

**Shell Responsibilities:**
*   **Navigation:** Global sidebar/header routing.
*   **Context Switching:** Workspace and Organization dropdown selectors.
*   **Notifications:** Global alert tray and unread badge management.
*   **User Profile:** Account management, password reset, avatar updates.
*   **Settings:** Centralized organization settings (billing, members, integrations).

Products simply provide a set of routes to be mounted within the main content area of the shell.

---

## 9. CONVERGENCE ROADMAP

The strategy safely evolves independent products into a platform over time.

### Phase 0: Product Stabilization (Current)
*   *Prerequisites:* None.
*   *Focus:* Complete AI Productivity OS activation path and stabilize AWDE independently.
*   *Risks:* Continued divergence of data models.
*   *Success Criteria:* Both products can reliably serve their core use case without crash loops.

### Phase 1: Contract Standardization
*   *Prerequisites:* Phase 0 complete.
*   *Focus:* Align data models. Ensure both products use the exact same `User` and `Organization` definitions. Implement unified JWT authentication.
*   *Risks:* Breaking existing auth flows.
*   *Success Criteria:* A user can log into either product with the same credentials.

### Phase 2: Shared Shell
*   *Prerequisites:* Phase 1 complete.
*   *Focus:* Build the React "Platform Shell". Move the routing, global nav, and organization settings into the shell. Mount OS and AWDE as sub-routes.
*   *Risks:* Complex UI state management; CSS clashes.
*   *Success Criteria:* Seamless UI transition between an Audit and a Workflow Diagnostic.

### Phase 3: Shared Services
*   *Prerequisites:* Phase 2 complete.
*   *Focus:* Extract billing, reporting, and notifications out of the products and into shared platform services communicating via events.
*   *Risks:* Distributed system complexity; event delivery failures.
*   *Success Criteria:* A single billing service meters usage for both Audits and Workflow Diagnostics.

### Phase 4: Unified Workspace
*   *Prerequisites:* Phase 3 complete.
*   *Focus:* Introduce the `Workspace` abstraction to group cross-product resources logically for users.
*   *Risks:* Complicating the user mental model.
*   *Success Criteria:* Users can view an Audit and a Workflow side-by-side in a single project folder.

### Phase 5: Public Platform Launch
*   *Prerequisites:* Phase 4 complete.
*   *Focus:* Expose platform APIs for external integrations.
*   *Risks:* Security vulnerabilities in public APIs.
*   *Success Criteria:* External systems can safely consume `AUDIT_COMPLETED` events.

---

## 10. ANTI-PATTERNS

We strictly prohibit the following "premature platformization" behaviors:

*   **Premature Platformization:** Building a generic "scoring engine" before we fully understand the specific rules of both the Audit and Workflow engines. Let the products define the engine first, then abstract it.
*   **Over-Abstraction:** Creating generic models like `Entity` or `Document` instead of explicit models like `Audit` or `Workflow`. Explicit is better than implicit.
*   **Duplicated Business Logic:** Allowing both products to implement their own "Send Email" logic. This creates maintenance nightmares. Use shared utilities or services for common operations.
*   **Shared Intelligence Engines:** Trying to make a single "AI Model" evaluate both an organizational audit and a workflow map. They are different domains. Keep the intelligence engines separated by product.
*   **Infrastructure-First Thinking:** Designing a Kafka event bus or a Kubernetes cluster before we have more than two simple web services. Solve the business problem first; scale the infrastructure when it actually hurts.
