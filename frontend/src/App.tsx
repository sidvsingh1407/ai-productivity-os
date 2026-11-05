import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ComingSoon from './pages/ComingSoon';
import Confirmed from './pages/Confirmed';
import Expired from './pages/Expired';
import Privacy from './pages/Privacy';
import Terms from './pages/Terms';
import Contact from './pages/Contact';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ComingSoon />} />
        <Route path="/confirmed" element={<Confirmed />} />
        <Route path="/expired" element={<Expired />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/terms" element={<Terms />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
