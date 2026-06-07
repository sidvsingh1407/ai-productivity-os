import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { toast } from 'sonner';
import { Copy, Plus, Trash2, Key, Activity, Clock } from 'lucide-react';

interface ApiKey {
  id: string;
  name: string;
  tier: string;
  is_active: boolean;
  created_at: string;
  last_used_at: string | null;
  expires_at: string | null;
}

interface ApiUsageLog {
  id: string;
  api_key_id: string;
  endpoint: string;
  request_method: string;
  response_status: number;
  latency_ms: number;
  created_at: string;
}

export function DeveloperDashboard() {
  const queryClient = useQueryClient();
  const [newKeyName, setNewKeyName] = useState('');
  const [showNewKeyModal, setShowNewKeyModal] = useState(false);
  const [newlyCreatedKey, setNewlyCreatedKey] = useState<{name: string, raw_key: string} | null>(null);

  const { data: apiKeys, isLoading: isLoadingKeys } = useQuery<ApiKey[]>({
    queryKey: ['api_keys'],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/platform/keys');
      return data;
    }
  });

  const { data: usageLogs, isLoading: isLoadingUsage } = useQuery<ApiUsageLog[]>({
    queryKey: ['api_usage'],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/platform/usage');
      return data;
    }
  });

  const createKeyMutation = useMutation({
    mutationFn: async (name: string) => {
      const { data } = await apiClient.post('/api/platform/keys', { name });
      return data;
    },
    onSuccess: (data) => {
      setNewlyCreatedKey({
        name: data.api_key.name,
        raw_key: data.raw_key
      });
      setNewKeyName('');
      setShowNewKeyModal(false);
      queryClient.invalidateQueries({ queryKey: ['api_keys'] });
      toast.success('API Key created successfully');
    },
    onError: () => {
      toast.error('Failed to create API Key');
    }
  });

  const revokeKeyMutation = useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/api/platform/keys/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['api_keys'] });
      toast.success('API Key revoked successfully');
    },
    onError: () => {
      toast.error('Failed to revoke API Key');
    }
  });

  const handleCreateKey = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName.trim()) return;
    createKeyMutation.mutate(newKeyName);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard');
  };

  return (
    <div className="max-w-5xl mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Developer Platform</h1>
        <p className="text-slate-500">Manage your API keys and monitor platform usage.</p>
      </div>

      {/* newly created key alert */}
      {newlyCreatedKey && (
        <div className="mb-8 p-6 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="text-green-800 font-semibold mb-2">API Key Created: {newlyCreatedKey.name}</h3>
          <p className="text-green-700 text-sm mb-4">
            Please copy your API key now. You will not be able to see it again!
          </p>
          <div className="flex items-center gap-2 bg-white p-3 border border-green-200 rounded">
            <code className="flex-1 text-slate-800">{newlyCreatedKey.raw_key}</code>
            <button
              onClick={() => copyToClipboard(newlyCreatedKey.raw_key)}
              className="p-2 hover:bg-slate-100 rounded text-slate-600 transition-colors"
            >
              <Copy className="w-4 h-4" />
            </button>
          </div>
          <button
            onClick={() => setNewlyCreatedKey(null)}
            className="mt-4 text-sm font-medium text-green-700 hover:text-green-800"
          >
            I have copied my key
          </button>
        </div>
      )}

      {/* Metrics Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 border border-slate-200 rounded-lg shadow-sm">
          <div className="flex items-center gap-3 text-slate-500 mb-2">
            <Key className="w-5 h-5" />
            <span className="font-medium">Active Keys</span>
          </div>
          <p className="text-3xl font-bold text-slate-900">
            {isLoadingKeys ? '-' : apiKeys?.length || 0}
          </p>
        </div>

        <div className="bg-white p-6 border border-slate-200 rounded-lg shadow-sm">
          <div className="flex items-center gap-3 text-slate-500 mb-2">
            <Activity className="w-5 h-5" />
            <span className="font-medium">Recent Requests</span>
          </div>
          <p className="text-3xl font-bold text-slate-900">
            {isLoadingUsage ? '-' : usageLogs?.length || 0}
          </p>
        </div>

        <div className="bg-white p-6 border border-slate-200 rounded-lg shadow-sm">
          <div className="flex items-center gap-3 text-slate-500 mb-2">
            <Clock className="w-5 h-5" />
            <span className="font-medium">Avg Latency</span>
          </div>
          <p className="text-3xl font-bold text-slate-900">
             {isLoadingUsage || !usageLogs?.length
               ? '-'
               : `${Math.round(usageLogs.reduce((acc, l) => acc + l.latency_ms, 0) / usageLogs.length)}ms`}
          </p>
        </div>
      </div>

      {/* API Keys Table */}
      <div className="bg-white border border-slate-200 rounded-lg shadow-sm mb-8 overflow-hidden">
        <div className="p-6 border-b border-slate-200 flex justify-between items-center bg-slate-50">
          <div>
            <h2 className="text-lg font-bold text-slate-900">API Keys</h2>
            <p className="text-sm text-slate-500">Keys used to authenticate API requests.</p>
          </div>
          <button
            onClick={() => setShowNewKeyModal(true)}
            className="flex items-center gap-2 bg-slate-900 text-white px-4 py-2 rounded-md font-medium hover:bg-slate-800 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Create Key
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-white border-b border-slate-200">
              <tr>
                <th className="px-6 py-4 font-medium text-slate-900">Name</th>
                <th className="px-6 py-4 font-medium text-slate-900">Tier</th>
                <th className="px-6 py-4 font-medium text-slate-900">Created</th>
                <th className="px-6 py-4 font-medium text-slate-900">Last Used</th>
                <th className="px-6 py-4 font-medium text-slate-900 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoadingKeys ? (
                <tr><td colSpan={5} className="px-6 py-8 text-center text-slate-500">Loading keys...</td></tr>
              ) : !apiKeys?.length ? (
                <tr><td colSpan={5} className="px-6 py-8 text-center text-slate-500">No API keys found. Create one to get started.</td></tr>
              ) : (
                apiKeys.map(key => (
                  <tr key={key.id} className="hover:bg-slate-50">
                    <td className="px-6 py-4 font-medium text-slate-900">{key.name}</td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 bg-slate-100 text-slate-600 rounded text-xs uppercase tracking-wider font-semibold">
                        {key.tier}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-slate-500">{new Date(key.created_at).toLocaleDateString()}</td>
                    <td className="px-6 py-4 text-slate-500">
                      {key.last_used_at ? new Date(key.last_used_at).toLocaleDateString() : 'Never'}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => {
                          if (confirm('Are you sure you want to revoke this key? Any applications using it will stop working immediately.')) {
                            revokeKeyMutation.mutate(key.id);
                          }
                        }}
                        className="p-2 text-slate-400 hover:text-red-600 transition-colors"
                        title="Revoke Key"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Usage Logs Table */}
      <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-200 bg-slate-50">
          <h2 className="text-lg font-bold text-slate-900">Recent API Requests</h2>
          <p className="text-sm text-slate-500">Log of the last 100 API requests made using your active keys.</p>
        </div>

        <div className="overflow-x-auto max-h-96">
          <table className="w-full text-left text-sm text-slate-600 relative">
            <thead className="bg-white border-b border-slate-200 sticky top-0">
              <tr>
                <th className="px-6 py-4 font-medium text-slate-900">Timestamp</th>
                <th className="px-6 py-4 font-medium text-slate-900">Method</th>
                <th className="px-6 py-4 font-medium text-slate-900">Endpoint</th>
                <th className="px-6 py-4 font-medium text-slate-900">Status</th>
                <th className="px-6 py-4 font-medium text-slate-900 text-right">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoadingUsage ? (
                <tr><td colSpan={5} className="px-6 py-8 text-center text-slate-500">Loading usage...</td></tr>
              ) : !usageLogs?.length ? (
                <tr><td colSpan={5} className="px-6 py-8 text-center text-slate-500">No requests recorded yet.</td></tr>
              ) : (
                usageLogs.map(log => (
                  <tr key={log.id} className="hover:bg-slate-50">
                    <td className="px-6 py-3 text-slate-500 whitespace-nowrap">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-3">
                      <span className="px-2 py-1 bg-slate-100 text-slate-600 rounded text-xs font-mono">
                        {log.request_method}
                      </span>
                    </td>
                    <td className="px-6 py-3 font-mono text-slate-700">{log.endpoint}</td>
                    <td className="px-6 py-3">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        log.response_status < 400 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                      }`}>
                        {log.response_status}
                      </span>
                    </td>
                    <td className="px-6 py-3 text-right text-slate-500">
                      {Math.round(log.latency_ms)}ms
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* New Key Modal */}
      {showNewKeyModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md overflow-hidden">
            <div className="p-6 border-b border-slate-200">
              <h3 className="text-xl font-bold text-slate-900">Create new API key</h3>
            </div>
            <form onSubmit={handleCreateKey}>
              <div className="p-6">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Key Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Production Backend"
                  value={newKeyName}
                  onChange={(e) => setNewKeyName(e.target.value)}
                  className="w-full border border-slate-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-slate-900"
                  autoFocus
                />
                <p className="mt-2 text-xs text-slate-500">
                  Give your key a descriptive name to help you identify it later.
                </p>
              </div>
              <div className="p-6 border-t border-slate-200 bg-slate-50 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowNewKeyModal(false)}
                  className="px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-200 rounded-md transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createKeyMutation.isPending || !newKeyName.trim()}
                  className="px-4 py-2 text-sm font-medium text-white bg-slate-900 hover:bg-slate-800 rounded-md transition-colors disabled:opacity-50"
                >
                  {createKeyMutation.isPending ? 'Creating...' : 'Create Key'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
