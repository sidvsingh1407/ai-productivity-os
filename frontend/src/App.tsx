import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';

// Pages placeholders
import Dashboard from './pages/Dashboard';
import NewAudit from './pages/NewAudit';
import AuditHistory from './pages/AuditHistory';
import AuditDetail from './pages/AuditDetail';
import NewWorkflow from './pages/NewWorkflow';
import WorkflowDetail from './pages/WorkflowDetail';
import IntegrationResults from './pages/IntegrationResults';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="audits">
            <Route index element={<AuditHistory />} />
            <Route path="new" element={<NewAudit />} />
            <Route path=":id" element={<AuditDetail />} />
          </Route>
          <Route path="workflows">
            <Route path="new" element={<NewWorkflow />} />
            <Route path=":id" element={<WorkflowDetail />} />
          </Route>
          <Route path="integration/:id" element={<IntegrationResults />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
