import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { OperationalNoticeModal } from './components/OperationalNoticeModal';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/audits/new" element={<PlaceholderPage title="Run AI Audit" />} />
        <Route path="/workflows/new" element={<PlaceholderPage title="Explore Workflow Diagnosis" />} />
      </Routes>
      <OperationalNoticeModal />
    </BrowserRouter>
  );
}

export default App;
