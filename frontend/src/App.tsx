import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { PrivateRoute } from './components/PrivateRoute';
import { AppShell } from './components/layout/AppShell';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import NewAudit from './pages/NewAudit';
import AuditDetail from './pages/AuditDetail';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route path="/" element={
          <PrivateRoute>
            <AppShell />
          </PrivateRoute>
        }>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="audits/new" element={<NewAudit />} />
          <Route path="audits/:id" element={<AuditDetail />} />
          {/* Add more private routes here */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
