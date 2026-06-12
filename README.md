
# TarkaX

## Overview

**Business Clarity for the AI Era**

TarkaX helps businesses discover what is actually slowing growth, creating operational friction, reducing productivity, and preventing AI investments from delivering value. Rather than focusing on AI hype, TarkaX provides operational intelligence and diagnostic tools to uncover hidden bottlenecks and reality gaps within your organization.

## Core Capabilities

*   **Workflow Diagnostic:** Analyze and identify inefficiencies in existing business processes.
*   **AI Audit:** Evaluate AI adoption and uncover hidden barriers to ROI.
*   **Prompt Improver:** Standardize and optimize AI interactions across teams.
*   **Dashboard & Reporting:** Gain visibility into operational friction with clear, actionable insights.
*   **Authentication System:** Secure user registration, organization management, and role-based access control.

## User Journey

Register → Verify Email → Login → Run Analysis → Review Findings → Access Dashboard

## Architecture

TarkaX is structured as a monorepo containing a modern React frontend and a robust FastAPI backend.

### Frontend
*   **Framework:** React 18 with Vite
*   **Routing:** React Router (handling public marketing pages, protected app routes, and admin routes)
*   **State Management:** Zustand (for authentication and global state)
*   **Styling:** Tailwind CSS with Radix UI components

### Backend
*   **Framework:** FastAPI (Python)
*   **Database Layer:** SQLAlchemy (asyncpg) connecting to PostgreSQL
*   **Authentication:** JWT-based authentication with role-based access control (RBAC)

### Infrastructure
*   **Deployment Platform:** Render (Backend) and Vercel (Frontend). Railway is available as an alternative deployment target.
*   **Background Tasks:** Celery with Redis for asynchronous processing (e.g., PDF generation, email sending).
*   **Email System:** SendGrid for transactional emails (verification, password reset).

## Project Structure

```text
.
├── backend/            # FastAPI application
│   ├── alembic/        # Database migrations
│   ├── models/         # SQLAlchemy database models
│   ├── tasks/          # Celery background tasks
│   └── [modules]/      # Feature-based routers and services (auth, audits, workflows, etc.)
├── frontend/           # React application
│   ├── src/
│   │   ├── api/        # API client and endpoints
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Page components
│   │   └── store/      # Zustand state stores
├── docs/               # Technical audits and architecture documents
└── README.md           # This file
```

## Authentication System

TarkaX uses a robust, JWT-based authentication system.

*   **Registration:** Users can sign up, creating a user record and an associated organization.
*   **Email Verification:** A verification link is sent via email (SendGrid) to activate the account.
*   **Login:** Users authenticate with email/password to receive access and refresh tokens.
*   **Logout:** Client-side token clearing and optional server-side invalidation.
*   **Password Management:** Full support for Forgot Password (email link), Reset Password, and Change Password flows.

## Current Status

### Production Readiness
TarkaX is actively being developed with core workflows functional.

**Known Issues & Limitations:**
*   Alembic SQLite support for JSONB columns is currently incomplete; local testing may rely on SQLAlchemy `create_all` or in-memory databases.
*   Certain background tasks (like PDF generation) rely on robust Redis availability; synchronous fallbacks are being refined.

## Roadmap

*   **Improved Observability & Monitoring:** Enhancing application telemetry and logging for better production insights.
*   **Expanded Reporting Capabilities:** Adding deeper analysis views and export options for diagnostic findings.
*   **Enhanced Operational Diagnostics:** Building more comprehensive workflows to identify business bottlenecks.

## Contributing

*   **Branch Strategy:** Create feature branches from `main` (e.g., `feature/add-new-diagnostic`).
*   **Pull Requests:** Ensure all new code includes appropriate tests and documentation updates. Verify changes against local environments before requesting review.
*   **Testing Requirements:** All PRs should pass existing Playwright and Pytest suites without regressions. Do not commit temporary test artifacts or databases.

## License

No formal license file (`LICENSE`) currently exists in the repository. All rights are reserved by default.
