import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient  from '@/api/client';
import { toast } from 'sonner';
import { Ban, CheckCircle2 } from 'lucide-react';

interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  organization: { name: string } | null;
  role: string;
  is_active: boolean;
}

export default function AdminUsers() {
  const [page, setPage] = useState(1);
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['admin', 'users', page],
    queryFn: async () => {
      const { data } = await apiClient.get(`/admin/users?page=${page}&limit=10`);
      return data; // { items: [...], total: 50, page: 1, pages: 5 }
    },
  });

  const deactivateMutation = useMutation({
    mutationFn: async (userId: string) => {
      await apiClient.put(`/admin/users/${userId}/deactivate`);
    },
    onSuccess: () => {
      toast.success('User deactivated successfully');
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] });
    },
    onError: () => {
      toast.error('Failed to deactivate user');
    },
  });

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-slate-900"></div>
      </div>
    );
  }

  const users: User[] = data?.items || [];
  const totalPages = data?.pages || 1;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Users</h1>
        <p className="text-sm text-slate-500">Manage all users across the platform.</p>
      </div>

      <div className="overflow-hidden rounded-lg border border-slate-200 shadow-sm" style={{ background: 'var(--tx-bg-card)' }}>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="border-b bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-6 py-4 font-medium">Name</th>
                <th className="px-6 py-4 font-medium">Email</th>
                <th className="px-6 py-4 font-medium">Organization</th>
                <th className="px-6 py-4 font-medium">Role</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 font-medium text-slate-900">
                    {user.first_name} {user.last_name}
                  </td>
                  <td className="px-6 py-4">{user.email}</td>
                  <td className="px-6 py-4">{user.organization?.name || 'N/A'}</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-800">
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {user.is_active ? (
                      <span className="inline-flex items-center text-green-600">
                        <CheckCircle2 className="mr-1.5 h-4 w-4" />
                        Active
                      </span>
                    ) : (
                      <span className="inline-flex items-center text-slate-500">
                        <Ban className="mr-1.5 h-4 w-4" />
                        Inactive
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    {user.is_active && (
                      <button
                        onClick={() => {
                          if (window.confirm('Are you sure you want to deactivate this user?')) {
                            deactivateMutation.mutate(user.id);
                          }
                        }}
                        disabled={deactivateMutation.isPending}
                        className="text-red-600 hover:text-red-800 disabled:opacity-50"
                      >
                        Deactivate
                      </button>
                    )}
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-slate-500">
                    No users found.
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
                className="rounded border border-slate-300 px-3 py-1 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-50" style={{ background: 'var(--tx-bg-card)' }}
              >
                Previous
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="rounded border border-slate-300 px-3 py-1 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-50" style={{ background: 'var(--tx-bg-card)' }}
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
