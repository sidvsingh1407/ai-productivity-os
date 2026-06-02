import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Select } from '@/components/ui/select';
import { AlertCircle, PlaySquare } from 'lucide-react';

export default function WorkflowDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [selectedAuditId, setSelectedAuditId] = useState('');

  const { data: workflow, isLoading, isError } = useQuery({
    queryKey: ['workflow', id],
    queryFn: async () => {
      const response = await apiClient.get(`/workflows/${id}`);
      return response.data;
    },
    enabled: !!id,
  });

  const { data: audits } = useQuery({
    queryKey: ['auditsList'],
    queryFn: async () => {
      const response = await apiClient.get(`/audits/?limit=100`);
      return response.data;
    },
  });

  const integrationMutation = useMutation({
    mutationFn: async (auditId: string) => {
      const response = await apiClient.post('/integrations/run', {
        audit_id: auditId,
        workflow_id: id,
      });
      return response.data;
    },
    onSuccess: (data) => {
      navigate(`/integrations/${data.id}`);
    },
  });

  if (isLoading) return <div>Loading workflow...</div>;
  if (isError) return <div>Error loading workflow.</div>;
  if (!workflow) return <div>Workflow not found.</div>;

  const auditsList = Array.isArray(audits) ? audits : audits?.items || [];
  const auditOptions = auditsList.map((a: any) => ({
    value: a.id,
    label: `${a.company_name} - ${new Date(a.created_at || Date.now()).toLocaleDateString()}`
  }));

  const handleRunIntegration = () => {
    if (selectedAuditId) {
      integrationMutation.mutate(selectedAuditId);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Workflow Diagnostic</h1>
          <p className="text-slate-500">ID: {id}</p>
        </div>
        <Badge variant={workflow.status === 'completed' ? 'default' : 'secondary'} className="text-sm px-3 py-1">
          {workflow.status?.toUpperCase() || 'UNKNOWN'}
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="col-span-1 md:col-span-2">
          <CardHeader>
            <CardTitle>Generated Blueprints</CardTitle>
            <CardDescription>Detected workflows and automation opportunities.</CardDescription>
          </CardHeader>
          <CardContent>
            {workflow.blueprints && workflow.blueprints.length > 0 ? (
              <div className="space-y-4">
                {workflow.blueprints.map((bp: any, idx: number) => (
                  <div key={idx} className="flex justify-between items-center p-4 border rounded-lg bg-white shadow-sm">
                    <div>
                      <div className="font-semibold text-slate-900">{bp.process_id || `Process ${idx + 1}`}</div>
                      <div className="text-sm text-slate-500 mt-1">
                        Automation Tier: <span className="font-medium">{bp.automation_tier || 'Unknown'}</span>
                      </div>
                    </div>
                    <div className="flex flex-col items-end">
                      <div className="flex items-center mb-2">
                        <span className="text-sm mr-2 text-slate-600">Confidence:</span>
                        <div className="w-24 bg-slate-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${bp.confidence >= 0.65 ? 'bg-green-500' : 'bg-yellow-500'}`}
                            style={{ width: `${(bp.confidence || 0) * 100}%` }}
                          />
                        </div>
                      </div>
                      {(bp.confidence || 0) < 0.65 && (
                        <Badge variant="secondary" className="text-xs">
                          <AlertCircle className="w-3 h-3 mr-1" /> Manual Review Required
                        </Badge>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-500">No blueprints generated yet.</p>
            )}
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Configuration Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between border-b pb-2">
                  <dt className="text-slate-500">Mode</dt>
                  <dd className="font-medium">{workflow.mode || 'N/A'}</dd>
                </div>
                {workflow.input_config && Object.entries(workflow.input_config).map(([key, val]) => (
                  <div key={key} className="flex justify-between border-b pb-2">
                    <dt className="text-slate-500">{key}</dt>
                    <dd className="font-medium">{String(val)}</dd>
                  </div>
                ))}
              </dl>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Run Integration Analysis</CardTitle>
              <CardDescription>Correlate these workflows with an audit result.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-1 block">Select Audit</label>
                <Select
                  value={selectedAuditId}
                  onChange={(e) => setSelectedAuditId(e.target.value)}
                  options={auditOptions}
                />
              </div>
              <Button
                className="w-full"
                onClick={handleRunIntegration}
                disabled={!selectedAuditId || integrationMutation.isPending || workflow.status !== 'completed'}
              >
                <PlaySquare className="mr-2 h-4 w-4" />
                {integrationMutation.isPending ? 'Running...' : 'Run Integration'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
