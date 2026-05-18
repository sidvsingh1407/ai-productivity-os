import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AppShell } from '@/components/layout/AppShell';
import { PrivateRoute } from '@/components/auth/PrivateRoute';
import { AdminRoute } from '@/components/admin/AdminRoute';
import { useAuthStore } from '@/store/authStore';

// Temporary Mock Login for testing
function Login() {
  const { setAuth } = useAuthStore();
  return (
    <div className="flex h-screen items-center justify-center bg-slate-50">
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <h1 className="mb-4 text-2xl font-bold">Login</h1>
        <button
          className="rounded bg-slate-900 px-4 py-2 text-white"
          onClick={() => {
            setAuth(
              { id: '1', email: 'admin@test.com', first_name: 'Admin', last_name: 'User', is_superadmin: true },
              { id: 'org_1', name: 'Test Org', slug: 'test-org' },
              'mock-access-token',
              'mock-refresh-token'
            );
            window.location.href = '/dashboard';
          }}
        >
          Login as Superadmin
        </button>
        <button
          className="ml-4 rounded bg-slate-200 px-4 py-2 text-slate-900"
          onClick={() => {
            setAuth(
              { id: '2', email: 'user@test.com', first_name: 'Regular', last_name: 'User', is_superadmin: false },
              { id: 'org_1', name: 'Test Org', slug: 'test-org' },
              'mock-access-token',
              'mock-refresh-token'
            );
            window.location.href = '/dashboard';
          }}
        >
          Login as User
        </button>
      </div>
    </div>
  );
}

// Temporary placeholders for pages until they are created
const Dashboard = () => <div>Dashboard Home</div>;
import Analytics from './pages/Analytics';
import AdminUsers from './pages/admin/AdminUsers';
import AdminOrgs from './pages/admin/AdminOrgs';
import OrgSettings from './pages/Settings/OrgSettings';
import Billing from './pages/Settings/Billing';

export default function App() {
  const { isAuthenticated } = useAuthStore();

  return (
    <Routes>
      <Route path="/login" element={!isAuthenticated() ? <Login /> : <Navigate to="/dashboard" />} />

      {/* Protected Routes */}
      <Route element={<PrivateRoute />}>
        <Route element={<AppShell />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings/org" element={<OrgSettings />} />
          <Route path="/settings/billing" element={<Billing />} />
        </Route>
      </Route>

      {/* Admin Routes */}
      <Route element={<AdminRoute />}>
        <Route element={<AppShell />}>
          <Route path="/admin/users" element={<AdminUsers />} />
          <Route path="/admin/orgs" element={<AdminOrgs />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
