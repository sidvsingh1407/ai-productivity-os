const fs = require('fs');

const content = `# Launch Readiness Audit

## 1. Executive Summary

**Launch Ready?** NO

**Why?** The application has critical frontend errors preventing users from accessing core authenticated experiences. A crash occurs in the \`Topbar\` component when \`user.full_name\` is undefined (the API returns \`name\`, not \`full_name\`), causing the entire app layout to crash. Additionally, User Journey 1 fails as the start audit button/form isn't visible due to these layout crashes or missing implementations, and Journey 4 times out looking for the exact contact form inputs.

## 2. Journey Scorecard

| Journey | Status |
| :--- | :--- |
| AI Audit | FAIL |
| Workflow Diagnostic | FAIL |
| Prompt Improver | FAIL |
| Contact Form | FAIL |
| Admin Panel | FAIL |

*Note: All authenticated journeys fail due to the global AppShell crash caused by the Topbar \`charAt\` TypeError.*

## 3. Critical Issues

1. **Global App Crash on Authenticated Routes:** The \`Topbar\` component attempts to read \`user.full_name.charAt(0)\`. Since the user object returned uses \`name\` rather than \`full_name\`, this throws a TypeError and triggers the React Error Boundary, completely blocking access to the Dashboard, AI Audit, Workflow Diagnostic, Prompt Improver, and Admin Panel.
2. **Contact Form Submission Fails:** The marketing contact page lacks the expected input fields (\`name\`, \`email\`, \`message\`), meaning users cannot successfully submit inquiries or leads.

## 4. High Priority Issues

1. **Missing Forms:** The \`/app/audits/new\` route does not render the necessary assessment form when bypassing the layout crash.
2. **Missing Analytics:** While packages are installed, actual runtime verification of analytics firing on core interactions could not be fully completed due to blocking crashes.

## 5. Medium Priority Issues

1. **Duplicate Navigation Links:** There are duplicate navigation links (one for desktop, one for footer/mobile) which caused minor ambiguity in automated testing, indicating possible slight visual duplication.

## 6. Low Priority Issues

1. None identified at this stage as testing is blocked by critical failures.

## 7. Recommended Action

**C. Delay Launch**

*Evidence:* The entire authenticated portion of the application crashes immediately upon load due to a frontend mapping error (\`user.full_name\` vs \`user.name\`). Until this is resolved, no core feature (AI Audit, Workflow Diagnostic, Prompt Improver) can be used or tested. Launching in this state would result in a 100% failure rate for logged-in users.
`;

fs.writeFileSync('LAUNCH_READINESS_AUDIT.md', content);
