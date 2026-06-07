# Frontend Page Map

## SECTION 1 — PAGE INVENTORY

| File Path | Route | Description | Links To | Components | Current Theme |
|---|---|---|---|---|---|
| `frontend/src/pages/NewWorkflow.tsx` | `/app/workflows/new` | Renders a page titled 'Run Workflow Diagnostic'. | None | Button, Card, CardContent, CardHeader, CardTitle... | Default Tailwind styles or empty |
| `frontend/src/pages/NewAudit.tsx` | `/app/audits/new` | Renders a page titled 'AI Readiness Diagnostic'. | None | Button, Input, Textarea, Check | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/WorkflowDetail.tsx` | `/app/workflows/:id` | Renders a page titled 'Workflow Diagnostic'. | None | Badge, Button, Card, CardContent, CardHeader... | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/Login.tsx` | `/login` | Renders UI components but no clear title found. | /dashboard, /register | Link, Navigate, Button, Input, Label... | Default Tailwind styles or empty |
| `frontend/src/pages/AuditDetail.tsx` | `/app/audits/:id` | Renders UI components but no clear title found. | None | ShieldAlert, ReportHeader, ExecutiveSummaryCard, AssessmentOverviewCard, ScoreBreakdown... | uses global background tokens, uses global text tokens, uses global typography classes, CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/Analytics.tsx` | `route unclear` | Renders a page titled 'Analytics Dashboard'. | None | ScoreTrendLine, Activity, BarChart2, ShieldCheck, Target | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/PlaceholderPage.tsx` | `route unclear` | Renders a page titled '{title}'. | / | None | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/AuditHistory.tsx` | `route unclear` | Renders a page titled 'Audit History'. | /audits/new | Table, TableBody, TableCell, TableHead, TableHeader... | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/InviteAcceptPage.tsx` | `route unclear` | Renders a page titled 'Invitation Failed'. | /app/dashboard, /login?redirect=/invite | Link | Default Tailwind styles or empty |
| `frontend/src/pages/PromptImprover.tsx` | `prompt-improver` | Renders a page titled 'Prompt Improver'. | None | Card, CardContent, CardHeader, CardTitle, CardDescription... | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/Dashboard.tsx` | `/app/dashboard` | Renders a page titled 'Decision Support Interface'. | /audits/new | BenchmarkIntelligenceCards | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/Register.tsx` | `/register` | Renders UI components but no clear title found. | /dashboard, /login | Link, Navigate, Button, Input, Label... | Default Tailwind styles or empty |
| `frontend/src/pages/IntegrationResults.tsx` | `integrations/:id` | Renders a page titled 'Integration Results'. | None | Card, CardContent, CardHeader, CardTitle, Badge... | Default Tailwind styles or empty |
| `frontend/src/pages/DeveloperDashboard.tsx` | `developers` | Renders a page titled 'Developer Platform'. | None | Copy, Plus, Trash2, Key, Activity... | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/Settings/OrgSettings.tsx` | `route unclear` | Renders a page titled 'Organization Settings'. | None | Mail, Trash2 | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/Settings/Billing.tsx` | `route unclear` | Renders a page titled 'Billing & Plans'. | None | Check | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/marketing/ResearchPage.tsx` | `route unclear` | Renders a page titled 'Research & Frameworks'. | None | BookOpen, FileText | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/marketing/AiDisclaimerPage.tsx` | `/ai-disclaimer` | Renders a page titled 'AI Transparency Disclaimer'. | None | SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/DeveloperPortal.tsx` | `/developers` | Renders a page titled 'TarkaX Developer Portal'. | None | None | uses global background tokens, uses global text tokens, CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/marketing/TrustPage.tsx` | `route unclear` | Renders a page titled 'Trust & Security Center'. | /contact?interest=Security | Shield, Lock, FileCheck, Eye, Link | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/marketing/AiAuditPage.tsx` | `/ai-audit` | Renders a page titled 'AI Audit'. | /contact?interest=Forecasting Framework, /sample-report, /contact?interest=AI+Audit, /workflow-diagnostic | Link, ArrowRight, CheckCircle2, SeoHead, DefinitionBlock... | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/TermsPage.tsx` | `/terms` | Renders a page titled 'Terms of Service'. | None | SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/AboutPage.tsx` | `/about` | Renders a page titled 'About TarkaX'. | /ai-audit, /contact, /workflow-diagnostic, # | Link, ArrowRight, SeoHead, DefinitionBlock | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/CookiesPage.tsx` | `/cookies` | Renders a page titled 'Cookie Policy'. | None | SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/SampleReportPage.tsx` | `/sample-report` | Renders a page titled 'Sample Report'. | /, /ai-audit, /contact | SeoHead, ReportHeader, ExecutiveSummaryCard, ScoreBreakdown, ShieldAlert... | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/BlogPage.tsx` | `/blog` | Renders a page titled 'Research & Insights'. | # | Link, SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/SecurityPage.tsx` | `/security` | Renders a page titled 'Security Overview'. | None | SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/Home.tsx` | `/` | Renders a page titled 'Operational Intelligence Platform'. | /sample-report, /ai-audit, /contact, /workflow-diagnostic | Link, ShieldAlert, ArrowRight, SeoHead, FAQSection | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/PrivacyPage.tsx` | `/privacy` | Renders a page titled 'Privacy Policy'. | None | SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/DataRetentionPage.tsx` | `/data-retention` | Renders a page titled 'Data Retention Policy'. | None | SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/ContactPage.tsx` | `/contact` | Renders a page titled 'Contact TarkaX'. | None | SeoHead | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/marketing/MethodologyPage.tsx` | `route unclear` | Renders a page titled 'The TarkaX Methodology'. | /ai-audit | ShieldCheck, Target, ArrowRight, Link | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/marketing/WorkflowDiagnosticPage.tsx` | `/workflow-diagnostic` | Renders a page titled 'Workflow Diagnostic'. | /forecasting, /ai-audit, /contact?interest=Workflow+Diagnostic | Link, ArrowRight, AlertTriangle, SeoHead, DefinitionBlock... | uses global background tokens, uses global text tokens, uses global typography classes |
| `frontend/src/pages/admin/AdminOrgs.tsx` | `route unclear` | Renders a page titled 'Organizations'. | None | None | CONFLICT: uses hardcoded Tailwind colors instead of tokens |
| `frontend/src/pages/admin/AdminUsers.tsx` | `route unclear` | Renders a page titled 'Users'. | None | Ban, CheckCircle2 | CONFLICT: uses hardcoded Tailwind colors instead of tokens |

## SECTION 2 — NAVIGATION MAP

```text
[ Global Layout: MarketingLayout ]
 ├─ /                     (Home)
 ├─ /ai-audit             (AiAuditPage)
 ├─ /workflow-diagnostic  (WorkflowDiagnosticPage)
 ├─ /about                (AboutPage)
 ├─ /blog                 (BlogPage)
 ├─ /contact              (ContactPage)
 ├─ /privacy              (PrivacyPage)
 ├─ /terms                (TermsPage)
 ├─ /cookies              (CookiesPage)
 ├─ /ai-disclaimer        (AiDisclaimerPage)
 ├─ /data-retention       (DataRetentionPage)
 ├─ /security             (SecurityPage)
 ├─ /developers           (DeveloperPortal)
 └─ /sample-report        (SampleReportPage)

[ Global Layout: Auth ]
 ├─ /login                (Login)
 └─ /register             (Register)

[ Global Layout: AppShell / Sidebar ]
 ├─ /app/dashboard        (Dashboard)
 ├─ /app/audits/new       (NewAudit)
 ├─ /app/workflows/new    (NewWorkflow)
 ├─ /app/prompt-improver  (PromptImprover)
 ├─ /app/audits           (AuditHistory)
 ├─ /app/developers       (DeveloperDashboard)
 └─ /app/settings         (Settings / Admin)

[ Dynamic / Inner Routes ]
 ├─ /app/audits/:id       (AuditDetail)
 ├─ /app/workflows/:id    (WorkflowDetail)
 └─ /app/integrations/:id (IntegrationResults)

[ Unlinked / Unreachable Flows ]
 ├─ prompt-improver (PromptImprover)
 ├─ integrations/:id (IntegrationResults)
 ├─ developers (DeveloperDashboard)
 ├─ /developers (DeveloperPortal)
```

## SECTION 3 — BROKEN OR DISCONNECTED PAGES

### `frontend/src/pages/PlaceholderPage.tsx`
- **Meaningless UI:** File exists but renders no significant components or is a placeholder.

### `frontend/src/pages/PromptImprover.tsx`
- **No inbound navigation links:** Page is not linked from any known global nav or other page.

### `frontend/src/pages/IntegrationResults.tsx`
- **No inbound navigation links:** Page is not linked from any known global nav or other page.

### `frontend/src/pages/DeveloperDashboard.tsx`
- **No inbound navigation links:** Page is not linked from any known global nav or other page.

### `frontend/src/pages/marketing/DeveloperPortal.tsx`
- **No inbound navigation links:** Page is not linked from any known global nav or other page.

### `frontend/src/pages/marketing/AboutPage.tsx`
- **Dead CTAs:** Page has buttons or links that do not perform actions (Empty href/to link).

### `frontend/src/pages/marketing/BlogPage.tsx`
- **Dead CTAs:** Page has buttons or links that do not perform actions (Empty href/to link).
