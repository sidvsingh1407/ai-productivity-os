import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { dependencyMapApi, DependencyEdgeCreate, NodeType, EdgeType } from '@/api/dependencyMap';
import { aiSystemsApi } from '@/api/aiSystems';
import { workflowsApi } from '@/api/workflows';
import { auditsApi } from '@/api/audits';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';

const NODE_TYPES: { value: NodeType; label: string }[] = [
  { value: 'ai_system', label: 'AI System' },
  { value: 'workflow', label: 'Workflow' },
  { value: 'audit', label: 'Audit' },
];

const EDGE_TYPES: { value: EdgeType; label: string }[] = [
  { value: 'uses', label: 'Uses' },
  { value: 'depends_on', label: 'Depends On' },
  { value: 'feeds_into', label: 'Feeds Into' },
  { value: 'integration', label: 'Integration' },
  { value: 'escalates_to', label: 'Escalates To' },
];

export default function DependencyMapForm() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  // Form State
  const [sourceType, setSourceType] = useState<NodeType | ''>('');
  const [sourceEntityId, setSourceEntityId] = useState<string>('');

  const [targetType, setTargetType] = useState<NodeType | ''>('');
  const [targetEntityId, setTargetEntityId] = useState<string>('');

  const [edgeType, setEdgeType] = useState<EdgeType | ''>('');

  // Queries to load entities for dropdowns
  const { data: systems = [] } = useQuery({ queryKey: ['ai-systems'], queryFn: aiSystemsApi.list });
  const { data: workflows = [] } = useQuery({ queryKey: ['workflows'], queryFn: workflowsApi.listWorkflows });
  const { data: auditsData } = useQuery({ queryKey: ['audits'], queryFn: auditsApi.listAudits });
  const audits = auditsData?.items || [];

  // Submit Mutation
  const createEdgeMutation = useMutation({
    mutationFn: async () => {
      // 1. Get or create source node
      const sourceNode = await dependencyMapApi.getOrCreateNode({
        node_type: sourceType as NodeType,
        ai_system_id: sourceType === 'ai_system' ? sourceEntityId : null,
        workflow_id: sourceType === 'workflow' ? sourceEntityId : null,
        audit_id: sourceType === 'audit' ? sourceEntityId : null,
      });

      // 2. Get or create target node
      const targetNode = await dependencyMapApi.getOrCreateNode({
        node_type: targetType as NodeType,
        ai_system_id: targetType === 'ai_system' ? targetEntityId : null,
        workflow_id: targetType === 'workflow' ? targetEntityId : null,
        audit_id: targetType === 'audit' ? targetEntityId : null,
      });

      // 3. Create edge
      const edgeData: DependencyEdgeCreate = {
        source_node_id: sourceNode.id,
        target_node_id: targetNode.id,
        edge_type: edgeType as EdgeType,
      };

      return dependencyMapApi.createEdge(edgeData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dependency-edges'] });
      queryClient.invalidateQueries({ queryKey: ['dependency-nodes'] });
      navigate('/app/dependency-map');
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || err.message || 'Failed to create relationship.');
    }
  });

  const getEntityOptions = (type: NodeType | '') => {
    if (type === 'ai_system') {
      return systems.map((s: any) => ({ value: s.id, label: s.name }));
    } else if (type === 'workflow') {
      return workflows.map((w: any) => ({ value: w.id, label: w.id })); // assuming workflow doesn't have name
    } else if (type === 'audit') {
      return audits.map((a: any) => ({ value: a.id, label: `Audit ${a.id.substring(0, 8)}` }));
    }
    return [];
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!sourceType || !sourceEntityId || !targetType || !targetEntityId || !edgeType) {
      setError("Please fill out all fields.");
      return;
    }
    createEdgeMutation.mutate();
  };

  const sourceOptions = getEntityOptions(sourceType);
  const targetOptions = getEntityOptions(targetType);

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Add Relationship</h1>
        <Button variant="outline" onClick={() => navigate('/app/dependency-map')}>Cancel</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Define Dependency Edge</CardTitle>
          <CardDescription>Link two entities in your organization to build the dependency map.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSave} className="space-y-6">
            {error && (
              <div className="bg-red-50 text-red-600 p-3 rounded text-sm">
                {error}
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Source Type</label>
                <select
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                  value={sourceType}
                  onChange={(e) => { setSourceType(e.target.value as NodeType); setSourceEntityId(''); }}
                  required
                >
                  <option value="">Select type...</option>
                  {NODE_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Source Entity</label>
                <select
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                  value={sourceEntityId}
                  onChange={(e) => setSourceEntityId(e.target.value)}
                  disabled={!sourceType}
                  required
                >
                  <option value="">Select entity...</option>
                  {sourceOptions.map((opt: any) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Relationship Type (Edge)</label>
              <select
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                value={edgeType}
                onChange={(e) => setEdgeType(e.target.value as EdgeType)}
                required
              >
                <option value="">Select relationship...</option>
                {EDGE_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Target Type</label>
                <select
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                  value={targetType}
                  onChange={(e) => { setTargetType(e.target.value as NodeType); setTargetEntityId(''); }}
                  required
                >
                  <option value="">Select type...</option>
                  {NODE_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Target Entity</label>
                <select
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                  value={targetEntityId}
                  onChange={(e) => setTargetEntityId(e.target.value)}
                  disabled={!targetType}
                  required
                >
                  <option value="">Select entity...</option>
                  {targetOptions.map((opt: any) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                </select>
              </div>
            </div>

            <Button type="submit" disabled={createEdgeMutation.isPending} className="w-full">
              {createEdgeMutation.isPending ? 'Saving...' : 'Save Relationship'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
