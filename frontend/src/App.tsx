import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Analytics } from "@vercel/analytics/react";
import { RouteTracker } from './components/analytics/RouteTracker';
import { PrivateRoute } from './components/PrivateRoute';
import { AppShell } from './components/layout/AppShell';
import { MarketingLayout } from './components/layout/MarketingLayout';

import Home from './pages/marketing/Home';
import AiAuditPage from './pages/marketing/AiAuditPage';
import WorkflowDiagnosticPage from './pages/marketing/WorkflowDiagnosticPage';
import AboutPage from './pages/marketing/AboutPage';
import PrivacyPage from './pages/marketing/PrivacyPage';
import SampleReportPage from './pages/marketing/SampleReportPage';
import TermsPage from './pages/marketing/TermsPage';
import CookiesPage from './pages/marketing/CookiesPage';
import AiDisclaimerPage from './pages/marketing/AiDisclaimerPage';
import DataRetentionPage from './pages/marketing/DataRetentionPage';
import SecurityPage from './pages/marketing/SecurityPage';
import BlogPage from './pages/marketing/BlogPage';
import ContactPage from "./pages/marketing/ContactPage";
import { DeveloperPortal } from "./pages/marketing/DeveloperPortal";

import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import NewAudit from './pages/NewAudit';
import AuditDetail from './pages/AuditDetail';
import NewWorkflow from './pages/NewWorkflow';
import WorkflowDetail from './pages/WorkflowDetail';
import IntegrationResults from "./pages/IntegrationResults";
import { DeveloperDashboard } from "./pages/DeveloperDashboard";
import PromptImprover from './pages/PromptImprover';

function App() {
  return (
    <>
      <BrowserRouter>
        <RouteTracker />
        <Routes>
          {/* Public Marketing Routes */}
        <Route element={<MarketingLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/ai-audit" element={<AiAuditPage />} />
          <Route path="/workflow-diagnostic" element={<WorkflowDiagnosticPage />} />
          <Route path="/forecasting" element={<Navigate to="/contact?interest=Forecasting Framework" replace />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/blog" element={<BlogPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/terms" element={<TermsPage />} />
          <Route path="/cookies" element={<CookiesPage />} />
          <Route path="/ai-disclaimer" element={<AiDisclaimerPage />} />
          <Route path="/data-retention" element={<DataRetentionPage />} />
          <Route path="/security" element={<SecurityPage />} />
          <Route path="/sample-report" element={<SampleReportPage />} />
          <Route path="/developers" element={<DeveloperPortal />} />
        </Route>

        {/* Auth Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route path="/app" element={
          <PrivateRoute>
            <AppShell />
          </PrivateRoute>
        }>
          <Route index element={<Navigate to="/app/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="audits/new" element={<NewAudit />} />
          <Route path="audits/:id" element={<AuditDetail />} />
          <Route path="workflows/new" element={<NewWorkflow />} />
          <Route path="workflows/:id" element={<WorkflowDetail />} />
          <Route path="integrations/:id" element={<IntegrationResults />} />
          <Route path="developers" element={<DeveloperDashboard />} />
          <Route path="prompt-improver" element={<PromptImprover />} />
        </Route>

        {/* Redirect old dashboard to new app dashboard */}
        <Route path="/dashboard" element={<Navigate to="/app/dashboard" replace />} />
        <Route path="/audits/*" element={<Navigate to={`/app/audits/${window.location.pathname.split('/').pop()}`} replace />} />
        <Route path="/workflows/*" element={<Navigate to={`/app/workflows/${window.location.pathname.split('/').pop()}`} replace />} />
        </Routes>
      </BrowserRouter>
      <Analytics />
    </>
  );
}

export default App;
