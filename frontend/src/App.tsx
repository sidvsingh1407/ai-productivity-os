
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from '@/pages/LandingPage';
import Dashboard from '@/pages/Dashboard';
import NewAudit from '@/pages/NewAudit';
import NewWorkflow from '@/pages/NewWorkflow';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/audits/new" element={<NewAudit />} />
        <Route path="/workflows/new" element={<NewWorkflow />} />
      </Routes>
    </BrowserRouter>
  );
}