import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/react";
import { RouteTracker } from './components/analytics/RouteTracker';
import { PrivateRoute } from './components/PrivateRoute';
import { AppShell } from './components/layout/AppShell';
import { MarketingLayout } from './components/layout/MarketingLayout';

import Home from './pages/marketing/Home';
import AiAuditPage from './pages/marketing/AiAuditPage';
import WorkflowDiagnosticPage from './pages/marketing/WorkflowDiagnosticPage';
import AboutPage from './pages/marketing/AboutPage';
import PrivacyPage from './pages/marketing/PrivacyPage';
import ExampleFindingsPage from './pages/marketing/resources/ExampleFindingsPage';
import TermsPage from './pages/marketing/TermsPage';
import CookiesPage from './pages/marketing/CookiesPage';

import AiRoiPage from './pages/marketing/problems/AiRoiPage';
import TeamProductivityPage from './pages/marketing/problems/TeamProductivityPage';
import OperationsChaoticPage from './pages/marketing/problems/OperationsChaoticPage';
import InconsistentAiPage from './pages/marketing/problems/InconsistentAiPage';
import ScaleWithoutHiringPage from './pages/marketing/problems/ScaleWithoutHiringPage';

import DiscoverBottlenecksPage from './pages/marketing/solutions/DiscoverBottlenecksPage';
import ImproveAiAdoptionPage from './pages/marketing/solutions/ImproveAiAdoptionPage';
import StandardizeAiOutputsPage from './pages/marketing/solutions/StandardizeAiOutputsPage';
import ReduceManualWorkPage from './pages/marketing/solutions/ReduceManualWorkPage';
import ImproveVisibilityPage from './pages/marketing/solutions/ImproveVisibilityPage';

import GuidesPage from './pages/marketing/resources/GuidesPage';
import CaseStudiesPage from './pages/marketing/resources/CaseStudiesPage';
import FaqPage from './pages/marketing/resources/FaqPage';
import PricingPage from './pages/marketing/PricingPage';

import AiDisclaimerPage from './pages/marketing/AiDisclaimerPage';
import DataRetentionPage from './pages/marketing/DataRetentionPage';
import SecurityPage from './pages/marketing/SecurityPage';
import BlogPage from './pages/marketing/BlogPage';
import ContactPage from "./pages/marketing/ContactPage";
import { DeveloperPortal } from "./pages/marketing/DeveloperPortal";

import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { ForgotPassword } from './pages/ForgotPassword';
import { ResetPassword } from './pages/ResetPassword';
import { VerifyEmail } from './pages/VerifyEmail';
import { Dashboard } from './pages/Dashboard';
import NewAudit from './pages/NewAudit';
import AuditDetail from './pages/AuditDetail';
import AuditHistory from './pages/AuditHistory';
import NewWorkflow from './pages/NewWorkflow';
import WorkflowDetail from './pages/WorkflowDetail';
import IntegrationResults from "./pages/IntegrationResults";
import { DeveloperDashboard } from "./pages/DeveloperDashboard";
import PromptImprover from './pages/PromptImprover';
import SettingsPage from './pages/Settings/SettingsPage';
import AiSystemsList from './pages/AiSystemsList';
import CapabilityMap from './pages/CapabilityMap';
import AiSystemForm from './pages/AiSystemForm';
import DependencyMapList from './pages/DependencyMapList';
import DependencyMapForm from './pages/DependencyMapForm';
import { AdminRoute } from './components/admin/AdminRoute';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminUsers from './pages/admin/AdminUsers';
import AdminOrgs from './pages/admin/AdminOrgs';

function App() {
  return (
    <>
      <BrowserRouter>
        <RouteTracker />
        <Routes>
          {/* Public Marketing Routes */}
        <Route element={<MarketingLayout />}>
          <Route path="/" element={<Home />} />

          {/* Problem Pages */}
          <Route path="/problems/ai-roi" element={<AiRoiPage />} />
          <Route path="/problems/team-productivity" element={<TeamProductivityPage />} />
          <Route path="/problems/operations-chaotic" element={<OperationsChaoticPage />} />
          <Route path="/problems/inconsistent-ai" element={<InconsistentAiPage />} />
          <Route path="/problems/scale-without-hiring" element={<ScaleWithoutHiringPage />} />

          {/* Solutions Pages */}
          <Route path="/solutions/discover-bottlenecks" element={<DiscoverBottlenecksPage />} />
          <Route path="/solutions/improve-ai-adoption" element={<ImproveAiAdoptionPage />} />
          <Route path="/solutions/standardize-ai-outputs" element={<StandardizeAiOutputsPage />} />
          <Route path="/solutions/reduce-manual-work" element={<ReduceManualWorkPage />} />
          <Route path="/solutions/improve-visibility" element={<ImproveVisibilityPage />} />

          {/* Legacy Marketing Routes */}
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

          {/* Resources & Pricing */}
          <Route path="/example-findings" element={<ExampleFindingsPage />} />
          <Route path="/resources/guides" element={<GuidesPage />} />
          <Route path="/resources/case-studies" element={<CaseStudiesPage />} />
          <Route path="/resources/faq" element={<FaqPage />} />
          <Route path="/pricing" element={<PricingPage />} />

          {/* Legacy route catch-all */}
          <Route path="/sample-report" element={<Navigate to="/example-findings" replace />} />
          <Route path="/developers" element={<DeveloperPortal />} />
        </Route>

        {/* Auth Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/verify-email" element={<VerifyEmail />} />

        {/* Protected Routes */}
        <Route path="/app" element={
          <PrivateRoute>
            <AppShell />
          </PrivateRoute>
        }>
          <Route index element={<Navigate to="/app/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="audits" element={<AuditHistory />} />
          <Route path="audits/new" element={<NewAudit />} />
          <Route path="audits/:id" element={<AuditDetail />} />
          <Route path="workflows/new" element={<NewWorkflow />} />
          <Route path="workflows/:id" element={<WorkflowDetail />} />
          <Route path="integrations/:id" element={<IntegrationResults />} />
          <Route path="developers" element={<DeveloperDashboard />} />
          <Route path="prompt-improver" element={<PromptImprover />} />
          <Route path="ai-systems" element={<AiSystemsList />} />
          <Route path="ai-systems/capability-map" element={<CapabilityMap />} />
          <Route path="ai-systems/new" element={<AiSystemForm />} />
          <Route path="ai-systems/:id/edit" element={<AiSystemForm />} />
          <Route path="dependency-map" element={<DependencyMapList />} />
          <Route path="dependency-map/new" element={<DependencyMapForm />} />
          <Route path="settings" element={<SettingsPage />} />

          {/* Admin Routes */}
          <Route path="admin" element={<AdminRoute />}>
            <Route index element={<AdminDashboard />} />
            <Route path="users" element={<AdminUsers />} />
            <Route path="orgs" element={<AdminOrgs />} />
          </Route>
        </Route>

        {/* Redirect old dashboard to new app dashboard */}
        <Route path="/dashboard" element={<Navigate to="/app/dashboard" replace />} />
        <Route path="/audits/*" element={<Navigate to={`/app/audits/${window.location.pathname.split('/').pop()}`} replace />} />
        <Route path="/workflows/*" element={<Navigate to={`/app/workflows/${window.location.pathname.split('/').pop()}`} replace />} />
        </Routes>
      </BrowserRouter>
      <Analytics />
      <SpeedInsights />
    </>
  );
}

export default App;
