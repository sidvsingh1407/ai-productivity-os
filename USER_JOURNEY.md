# TarkhaX Platform User Journey

Based on the implemented codebase, here is the complete user journey and the features that are currently available to the user.

## 1. Landing Experience
When a user first visits the application at the root (`/`), they are presented with a public cinematic landing page.
- The page features a premium "cinematic editorial" and "executive-grade analytical" aesthetic (Gold, Teal, Emerald, Red, dark atmospheric elements).
- It highlights sections like:
  - **Maturity Radar** (Module 01)
  - **Workflow Diagnosis** (Module 02)
  - **Integration Intelligence** (Dashboard preview)
  - **Governance-First Architecture**
- At the bottom, there is an "Access Intelligence Dashboard" Call-to-Action. Clicking this navigates the user toward the platform (`/dashboard`).
- *Note:* A generic **Operational Intelligence Notice** disclaimer modal may appear (depending on component usage) that traps focus and warns the user about data privacy and the nature of AI recommendations. Users must acknowledge this to proceed.

## 2. Registration and Login Flow
If the user is not authenticated, attempting to access the platform redirects them to the authentication flow.

### Registration (`/register`)
- The user is asked to provide:
  - Full Name
  - Company Name
  - Email
  - Password
- Upon successful registration, the user is either auto-logged in and redirected to the dashboard, or sent to the login page.

### Login (`/login`)
- The user is asked to provide:
  - Email
  - Password
- Upon success, the user is redirected to the authenticated platform (`/dashboard`).

## 3. The Dashboard (`/dashboard`)
Once authenticated, the user enters the App Shell, which includes a Sidebar (navigation) and a Topbar (showing their name and organization).
The dashboard greets the user by name and displays:
- **Two Primary Actions:** "Run AI Audit" and "Run Workflow Diagnostic"
- **High-level Stats:**
  - Total Audits (Lifetime audits run)
  - Last Score (Latest audit performance)
  - Compliance Status (Overall compliance health)

## 4. Running an Audit
- Currently, the page to initiate a new audit (`/audits/new` mapped to `NewAudit.tsx`) is a **placeholder page**. It shows the text: "Optimization Audit Engine. Audit initialization sequence would go here." The actual interactive form for asking audit questions is *currently non-functional* in the UI.
- However, users can view past audits via the **Audit History** page (`/audits`), which displays a table of previous audits showing Date, Company, Total Score, Rating, Compliance Risk status, and a "View" button.

## 5. Viewing Audit Results
When a user clicks into a specific audit from the history (`/audits/:id`), they see the Audit Detail view:
- **Header info:** Company name and ID.
- **Actions:**
  - "Download PDF" (generates and downloads a report)
  - "Run Workflow Diagnostic"
- **Warnings:** A red Compliance Alert banner is shown if compliance risk flags are detected.
- **Scores Displayed:**
  - **Total Score:** A large numerical score (e.g., out of 100).
  - **Rating:** A text rating badge (colored green, yellow, or red based on the score).
  - **Score Breakdown (Radar Chart):** A chart visualizing 5 dimensions.
  - **Dimensions Details (Bar Charts):** Individual scores for:
    - Awareness
    - Adoption
    - Integration
    - Governance
    - ROI

## 6. Running a Workflow Diagnostic
- Similar to New Audits, the page to create a new workflow (`/workflows/new` mapped to `NewWorkflow.tsx`) is currently a **placeholder page**.
- Users can view a specific workflow diagnostic result on the **Workflow Detail** page (`/workflows/:id`).
- On this page, the user sees:
  - Workflow ID and Status badge (e.g., COMPLETED).
  - **Generated Blueprints:** A list of detected workflows/automation opportunities showing a Process ID, Automation Tier, and a visual Confidence bar. Low confidence items receive a "Manual Review Required" badge.
  - **Configuration Summary:** Key/value pairs showing how the workflow was run (e.g., Mode).
  - **Run Integration Analysis:** A form to correlate the workflow with an existing audit. The user selects a past audit from a dropdown and clicks "Run Integration".

## 7. Viewing Integrated Results and Recommendations
After running an integration (correlating a workflow with an audit), the user is taken to the **Integration Results** page (`/integration/:id`).
- **Audit Summary:** Shows the total score, rating, and dimension breakdowns of the selected audit.
- **Recommendations & Action Items:** A categorized list of actionable insights grouped by priority:
  - High Priority (red)
  - Medium Priority (yellow)
  - Low Priority (blue)
- Items flagged for compliance risks show a specific warning badge and warning text.

## 8. Analytics Dashboard (`/analytics`)
The Analytics view provides a higher-level overview of the organization's performance:
- **Stat Cards:**
  - Total Audits
  - Average Score
  - Compliance Rate
  - Audits This Month
- **Charts:**
  - **Score Trend Line:** A line chart showing audit scores over time.
  - **Dimension Averages:** Progress bars showing the organization's average scores across the 5 dimensions (Awareness, Adoption, Integration, Governance, ROI).

## 9. Admin Panel Capabilities
Users with the appropriate permissions can access administrative tools:
- **Organizations (`/admin/orgs`):** A table listing all organizations on the platform, showing Org Name, Slug, Member Count, and Created Date.
- **Users (`/admin/users`):** A table listing all users across the platform, showing Name, Email, Organization, Role, and Status (Active/Inactive). Admins have a functional action to "Deactivate" active users.

## 10. Settings and Billing
- **Organization Settings (`/settings/org`):**
  - Displays the Organization Name (currently marked as non-editable).
  - **Team Members:** A table listing current members and their roles.
  - **Actions:** The user can invite new members via email (sends an invitation) or remove existing members from the organization.
- **Billing & Plans (`/settings/billing`):**
  - Displays the current "Free Plan" features.
  - Shows an "Upgrade to Pro" section. Clicking the upgrade button triggers a notification stating: "Billing configuration coming soon. We are currently setting up our payment provider." (This feature is *currently non-functional*).
