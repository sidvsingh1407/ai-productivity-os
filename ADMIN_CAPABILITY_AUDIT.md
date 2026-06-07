# Admin Capability Audit

## Current State

TarkaX currently possesses a foundational but very limited set of Platform Administrator capabilities. The system supports a `is_superadmin` flag on the `User` model, which gates access to a dedicated backend router (`/admin`). The frontend contains rudimentary views for an administrator to list users and organizations.

Currently, the Prompt Improver is completely stateless. It accepts a request, processes it, and returns the response without persisting usage data, prompts, context classifications, or validation failures to the database. API keys and API usage logging exist conceptually but are scoped to Organization Admins, lacking a platform-wide oversight view.

## Existing Admin Functionality

### Backend (`/admin` router)
- **View Users:** List all platform users (`GET /admin/users`)
- **View Organizations:** List all platform organizations (`GET /admin/orgs`)
- **Deactivate User:** Soft-delete a user (`PUT /admin/users/{id}/deactivate`)
- **System Stats:** Get aggregate counts for total users, orgs, audits, workflows, and audits this month (`GET /admin/stats`)

### Frontend
- **Admin Users Page (`/admin/users`):** Displays a paginated table of users and a button to deactivate.
- **Admin Orgs Page (`/admin/orgs`):** Displays a paginated table of organizations.
*Note: The frontend admin pages are currently unreachable via navigation. They exist in the codebase but are not wired into `App.tsx` routing or the Sidebar menu.*

### Database
- **Role:** `is_superadmin` flag on the `User` model.

## Missing Admin Functionality

The following operational capabilities are entirely missing or inaccessible without direct database queries:

1. **Accessing Admin Views:** No frontend routing or navigation menu exists for the platform admin pages.
2. **Contact Leads Management:** No way to view or manage form submissions from the `contact_leads` table.
3. **Audit Oversight:** No way to view individual audit details, status, or scores across all organizations.
4. **Workflow Diagnostic Oversight:** No way to view generated blueprints or workflow statuses.
5. **Prompt Improver Monitoring:** The engine is stateless; there is no database schema or admin view for monitoring volume, context classifications, validation failures, or most requested improvements.
6. **Platform API Oversight:** No global view of API key usage, rate limiting hits, or endpoint performance across all organizations.

## Launch-Critical Admin Features

To successfully operate the platform for 100-1000 users without direct database access, the following Admin MVP must be implemented before the public SaaS launch:

1. **Admin Navigation:** Wire the existing `/admin/users` and `/admin/orgs` pages into a protected route (`/admin`) and provide a navigation entry in the Sidebar (visible only to `is_superadmin`).
2. **Platform Dashboard (Stats):** Create a simple UI to consume the existing `GET /admin/stats` endpoint to monitor overall system growth.
3. **Contact Leads Viewer:** Create a backend endpoint and frontend table to view `contact_leads` to allow the sales/support team to respond to inbound inquiries.
4. **Prompt Improver Telemetry (Basic):** Implement a lightweight, asynchronous logging mechanism (e.g., FastAPI `BackgroundTasks`) to record Prompt Improver requests (timestamp, context classified, validation pass/fail, error reason). *Do not store PII or the raw prompt text unless required, but capture metadata for operational visibility.*
5. **Audit / Workflow Viewer:** Create read-only platform views to list recent Audits and Workflows, their statuses, and associated organizations, enabling support teams to troubleshoot failed generations.

## Post-Launch Admin Features

Capabilities that can be deferred until after the initial public launch:

1. **Advanced Telemetry & Analytics:** Deep dive intelligence into the most common prompt categories and operational failures.
2. **Platform API Usage Dashboard:** Global oversight of API usage, rate limits, and latency metrics across all tenants.
3. **Impersonation:** Ability for superadmins to "log in as" a user for deep troubleshooting.
4. **Billing & Subscription Oversight:** Managing Stripe/billing states from within the TarkaX admin panel.
5. **Organization Admin Enhancements:** Customer RBAC, team hierarchies, and permission matrices.

## Recommended Admin MVP

**Goal:** Operate the platform for 1000 users, handle support tickets, and monitor Prompt Improver stability without needing a SQL client.

1. **Routing & Access:** Create a `/admin` route group in `App.tsx` restricted to users with `is_superadmin = true`. Add an "Admin Panel" button to the Sidebar.
2. **Dashboard:** A simple landing page for admins showing `GET /admin/stats`.
3. **Users & Orgs:** Expose the existing `AdminUsers.tsx` and `AdminOrgs.tsx` components.
4. **Lead Management:** Build a `Contact Leads` table to view the `contact_leads` table.
5. **Prompt Improver Telemetry:** Add a `prompt_telemetry` table. Log timestamp, context category, execution risks found, validation passed (bool), and validation errors. Build a simple admin view to monitor this table for failure spikes.

## Recommended Build Order

1. **Phase 1: Routing & Existing Assets (1 day)**
   - Wire up `App.tsx` and Sidebar for superadmins.
   - Build the basic stats dashboard.
2. **Phase 2: Contact & Support (1-2 days)**
   - Build backend route for `GET /admin/leads`.
   - Build frontend `AdminLeads.tsx`.
   - Build backend route `GET /admin/audits` (read-only).
   - Build frontend `AdminAudits.tsx`.
3. **Phase 3: Prompt Improver Telemetry (2-3 days)**
   - Create `PromptTelemetry` SQLAlchemy model.
   - Generate Alembic migration.
   - Update `PromptIntelligenceService` to write telemetry asynchronously.
   - Build frontend `AdminPromptUsage.tsx` to monitor volume and failure rates.