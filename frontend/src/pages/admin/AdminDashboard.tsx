import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import apiClient from '@/api/client';
import { Users, Building2, FileText, GitBranch, ShieldAlert, Activity } from 'lucide-react';

interface SystemStats {
  total_users: number;
  total_orgs: number;
  total_audits: number;
  total_workflows: number;
  audits_this_month: number;
}

export default function AdminDashboard() {
  const { data: stats, isLoading } = useQuery<SystemStats>({
    queryKey: ['admin', 'stats'],
    queryFn: async () => {
      const { data } = await apiClient.get('/admin/stats');
      return data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-slate-900"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Platform Overview</h1>
        <p className="text-sm text-slate-500">Global statistics and administration.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {/* Stats Cards */}
        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-md bg-blue-50 p-3 text-blue-600">
              <Users className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">Total Users</p>
              <p className="text-2xl font-bold text-slate-900">{stats?.total_users || 0}</p>
            </div>
          </div>
        </div>

        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-md bg-purple-50 p-3 text-purple-600">
              <Building2 className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">Organizations</p>
              <p className="text-2xl font-bold text-slate-900">{stats?.total_orgs || 0}</p>
            </div>
          </div>
        </div>

        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-md bg-emerald-50 p-3 text-emerald-600">
              <FileText className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">Total Audits</p>
              <p className="text-2xl font-bold text-slate-900">{stats?.total_audits || 0}</p>
            </div>
          </div>
        </div>

        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-md bg-amber-50 p-3 text-amber-600">
              <GitBranch className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">Workflow Intelligence</p>
              <p className="text-2xl font-bold text-slate-900">{stats?.total_workflows || 0}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Quick Actions */}
        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 bg-slate-50 px-6 py-4">
            <h3 className="font-medium text-slate-900">Quick Actions</h3>
          </div>
          <div className="divide-y divide-slate-100">
            <Link to="/app/admin/users" className="flex items-center justify-between p-6 hover:bg-slate-50">
              <div className="flex items-center gap-4">
                <div className="rounded-md bg-slate-100 p-2 text-slate-600">
                  <Users className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-medium text-slate-900">Manage Users</p>
                  <p className="text-sm text-slate-500">View and manage platform users</p>
                </div>
              </div>
              <span className="text-slate-400">&rarr;</span>
            </Link>

            <Link to="/app/admin/orgs" className="flex items-center justify-between p-6 hover:bg-slate-50">
              <div className="flex items-center gap-4">
                <div className="rounded-md bg-slate-100 p-2 text-slate-600">
                  <Building2 className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-medium text-slate-900">Manage Organizations</p>
                  <p className="text-sm text-slate-500">View and manage organizations</p>
                </div>
              </div>
              <span className="text-slate-400">&rarr;</span>
            </Link>
          </div>
        </div>

        {/* Upcoming Capabilities */}
        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 bg-slate-50 px-6 py-4">
            <h3 className="font-medium text-slate-900">Upcoming Capabilities</h3>
          </div>
          <div className="divide-y divide-slate-100 opacity-60">
            <div className="flex items-center justify-between p-6">
              <div className="flex items-center gap-4">
                <div className="rounded-md bg-slate-100 p-2 text-slate-600">
                  <Activity className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-medium text-slate-900">Leads</p>
                  <p className="text-sm text-slate-500">Manage inbound interest</p>
                </div>
              </div>
              <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-800">
                Coming Soon
              </span>
            </div>

            <div className="flex items-center justify-between p-6">
              <div className="flex items-center gap-4">
                <div className="rounded-md bg-slate-100 p-2 text-slate-600">
                  <ShieldAlert className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-medium text-slate-900">Audit Monitoring</p>
                  <p className="text-sm text-slate-500">Monitor audit performance globally</p>
                </div>
              </div>
              <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-800">
                Coming Soon
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
