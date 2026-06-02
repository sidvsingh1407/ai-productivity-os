import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient  from '@/api/client';
import { useAuthStore } from '@/store/authStore';
import { toast } from 'sonner';
import { Mail, Trash2 } from 'lucide-react';

interface Member {
  id: string;
  user: {
    first_name: string;
    last_name: string;
    email: string;
  };
  role: string;
}

export default function OrgSettings() {
  const { organization } = useAuthStore();
  const queryClient = useQueryClient();
  const [inviteEmail, setInviteEmail] = useState('');

  const { data: members, isLoading } = useQuery<Member[]>({
    queryKey: ['org', 'members'],
    queryFn: async () => {
      const { data } = await apiClient.get('/org/members');
      return data;
    },
  });

  const inviteMutation = useMutation({
    mutationFn: async (email: string) => {
      await apiClient.post('/org/invite', { email });
    },
    onSuccess: () => {
      toast.success('Invitation sent successfully');
      setInviteEmail('');
      queryClient.invalidateQueries({ queryKey: ['org', 'members'] });
    },
    onError: () => {
      toast.error('Failed to send invitation');
    },
  });

  const removeMemberMutation = useMutation({
    mutationFn: async (memberId: string) => {
      await apiClient.delete(`/org/members/${memberId}`);
    },
    onSuccess: () => {
      toast.success('Member removed successfully');
      queryClient.invalidateQueries({ queryKey: ['org', 'members'] });
    },
    onError: () => {
      toast.error('Failed to remove member');
    },
  });

  const handleInvite = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteEmail) return;
    inviteMutation.mutate(inviteEmail);
  };

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Organization Settings</h1>
        <p className="text-sm text-slate-500">Manage your organization details and team members.</p>
      </div>

      {/* Org Details */}
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-medium text-slate-900">Organization Details</h2>
        <div className="max-w-md space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700">Organization Name</label>
            <input
              type="text"
              disabled
              value={organization?.name || ''}
              className="mt-1 block w-full rounded-md border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-500 shadow-sm focus:border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-500 disabled:opacity-50"
            />
            <p className="mt-1 text-xs text-slate-500">Editing organization name will be available soon.</p>
          </div>
        </div>
      </div>

      {/* Team Members */}
      <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 p-6">
          <h2 className="text-lg font-medium text-slate-900">Team Members</h2>
          <p className="mt-1 text-sm text-slate-500">Invite new members or manage existing ones.</p>

          <form onSubmit={handleInvite} className="mt-4 flex max-w-md gap-2">
            <div className="relative flex-1">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <Mail className="h-4 w-4 text-slate-400" />
              </div>
              <input
                type="email"
                required
                value={inviteEmail}
                onChange={(e) => setInviteEmail(e.target.value)}
                placeholder="Email address"
                className="block w-full rounded-md border border-slate-300 py-2 pl-10 pr-3 text-sm shadow-sm focus:border-slate-900 focus:outline-none focus:ring-1 focus:ring-slate-900"
              />
            </div>
            <button
              type="submit"
              disabled={inviteMutation.isPending || !inviteEmail}
              className="inline-flex items-center justify-center rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-slate-800 disabled:opacity-50"
            >
              {inviteMutation.isPending ? 'Inviting...' : 'Invite'}
            </button>
          </form>
        </div>

        {isLoading ? (
          <div className="p-8 text-center text-slate-500">Loading members...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-50 text-xs uppercase text-slate-500">
                <tr>
                  <th className="px-6 py-4 font-medium">Member</th>
                  <th className="px-6 py-4 font-medium">Role</th>
                  <th className="px-6 py-4 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {members?.map((member) => (
                  <tr key={member.id} className="hover:bg-slate-50">
                    <td className="px-6 py-4">
                      <div className="font-medium text-slate-900">
                        {member.user.first_name} {member.user.last_name}
                      </div>
                      <div className="text-slate-500">{member.user.email}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-800">
                        {member.role}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => {
                          if (window.confirm('Remove this member?')) {
                            removeMemberMutation.mutate(member.id);
                          }
                        }}
                        disabled={removeMemberMutation.isPending}
                        className="text-slate-400 hover:text-red-600 disabled:opacity-50"
                        title="Remove member"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
                {members?.length === 0 && (
                  <tr>
                    <td colSpan={3} className="px-6 py-8 text-center text-slate-500">
                      No members found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
