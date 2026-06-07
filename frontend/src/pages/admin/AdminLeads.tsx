import { useState, useMemo } from "react";
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { format } from 'date-fns';

interface Lead {
  id: string;
  name: string;
  email: string;
  company: string | null;
  interest: string | null;
  status: string;
  created_at: string;
}

export default function AdminLeads() {
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");

  const limit = 100; // Fetch up to 100 leads per request

  const { data, isLoading, isError } = useQuery({
    queryKey: ['admin', 'leads', page],
    queryFn: async () => {
      // Backend expects skip and limit
      const skip = (page - 1) * limit;
      const { data } = await apiClient.get(`/admin/leads?skip=${skip}&limit=${limit}`);
      return data; // { items: [...], total_count: 57 }
    },
  });

  const allLeads: Lead[] = data?.items || [];

  // Frontend filtering
  const filteredLeads = useMemo(() => {
    return allLeads.filter((lead) => {
      // Search filter
      const searchLower = searchQuery.toLowerCase();
      const matchesSearch =
        lead.name.toLowerCase().includes(searchLower) ||
        lead.email.toLowerCase().includes(searchLower) ||
        (lead.company?.toLowerCase() || "").includes(searchLower);

      // Status filter
      const matchesStatus = statusFilter === "All" || lead.status.toLowerCase() === statusFilter.toLowerCase();

      return matchesSearch && matchesStatus;
    });
  }, [allLeads, searchQuery, statusFilter]);

  const totalPages = data?.total_count ? Math.ceil(data.total_count / limit) : 1;

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-slate-900"></div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex h-64 items-center justify-center text-red-500">
        Failed to load leads.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Leads</h1>
        <p className="text-sm text-slate-500">View contact form submissions.</p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-4">
        <input
          type="text"
          placeholder="Search by name, email, or company..."
          className="rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 flex-1"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <select
          className="rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 w-full sm:w-48"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="All">All Statuses</option>
          <option value="New">New</option>
          <option value="Contacted">Contacted</option>
          <option value="Qualified">Qualified</option>
          <option value="Closed">Closed</option>
        </select>
      </div>

      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="border-b bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-6 py-4 font-medium">Name</th>
                <th className="px-6 py-4 font-medium">Email</th>
                <th className="px-6 py-4 font-medium">Company</th>
                <th className="px-6 py-4 font-medium">Interest</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredLeads.map((lead) => (
                <tr key={lead.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 font-medium text-slate-900">
                    {lead.name}
                  </td>
                  <td className="px-6 py-4">{lead.email}</td>
                  <td className="px-6 py-4">{lead.company || '-'}</td>
                  <td className="px-6 py-4">{lead.interest || '-'}</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-800 capitalize">
                      {lead.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {format(new Date(lead.created_at), 'MMM d, yyyy HH:mm')}
                  </td>
                </tr>
              ))}
              {filteredLeads.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-slate-500">
                    No leads found matching your filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between border-t px-6 py-3">
            <span className="text-sm text-slate-500">
              Page {page} of {totalPages}
            </span>
            <div className="space-x-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="rounded border border-slate-300 bg-white px-3 py-1 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                Previous
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="rounded border border-slate-300 bg-white px-3 py-1 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
