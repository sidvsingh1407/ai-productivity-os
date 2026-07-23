import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Select } from '@/components/ui/select';
import { AlertCircle, PlaySquare, CheckCircle, AlertTriangle, TrendingUp } from 'lucide-react';

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
      navigate(`/app/workflows/${data.id}`);
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

  const hasNewDiagnosticResults = workflow.scores && workflow.findings;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            {workflow.input_config?.workflow_name || 'Workflow Intelligence'}
          </h1>
          <p className="text-slate-500">ID: {id}</p>
        </div>
        <Badge variant={workflow.status === 'completed' ? 'default' : 'secondary'} className="text-sm px-3 py-1">
          {workflow.status?.toUpperCase() || 'UNKNOWN'}
        </Badge>
      </div>

      {hasNewDiagnosticResults && (
        <Card className="mb-6 border-l-4 border-l-indigo-600">
          <CardHeader>
            <CardTitle>Diagnostic Results</CardTitle>
            <CardDescription>Deterministic scoring and findings based on step analysis</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="p-4 bg-slate-50 rounded-lg text-center border">
                <div className="text-sm text-slate-500 mb-1">Health</div>
                <div className="font-semibold text-2xl text-slate-900">{workflow.scores.health}</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg text-center border">
                <div className="text-sm text-slate-500 mb-1">Bottleneck</div>
                <div className="font-semibold text-2xl text-slate-900">{workflow.scores.bottleneck}</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg text-center border">
                <div className="text-sm text-slate-500 mb-1">Ambiguity</div>
                <div className="font-semibold text-2xl text-slate-900">{workflow.scores.ambiguity}</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg text-center border">
                <div className="text-sm text-slate-500 mb-1">Governance</div>
                <div className="font-semibold text-2xl text-slate-900">{workflow.scores.governance}</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg text-center border">
                <div className="text-sm text-slate-500 mb-1">Risk</div>
                <div className="font-semibold text-2xl text-slate-900">{workflow.scores.risk}</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="space-y-3">
                <h3 className="font-semibold flex items-center text-green-700">
                  <CheckCircle className="w-5 h-5 mr-2" /> Strengths
                </h3>
                {workflow.findings.strengths && workflow.findings.strengths.length > 0 ? (
                  <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
                    {workflow.findings.strengths.map((s: string, idx: number) => (
                      <li key={idx}>{s}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-slate-500 italic">No specific strengths identified.</p>
                )}
              </div>

              <div className="space-y-3">
                <h3 className="font-semibold flex items-center text-amber-700">
                  <AlertTriangle className="w-5 h-5 mr-2" /> Weaknesses
                </h3>
                {workflow.findings.weaknesses && workflow.findings.weaknesses.length > 0 ? (
                  <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
                    {workflow.findings.weaknesses.map((w: string, idx: number) => (
                      <li key={idx}>{w}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-slate-500 italic">No significant weaknesses identified.</p>
                )}
              </div>

              <div className="space-y-3">
                <h3 className="font-semibold flex items-center text-blue-700">
                  <TrendingUp className="w-5 h-5 mr-2" /> Priority Actions
                </h3>
                {workflow.findings.priority_actions && workflow.findings.priority_actions.length > 0 ? (
                  <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
                    {workflow.findings.priority_actions.map((p: string, idx: number) => (
                      <li key={idx}>{p}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-slate-500 italic">No priority actions recommended.</p>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {!hasNewDiagnosticResults && workflow.intelligence && (
        <Card className="mb-6 border-l-4 border-l-blue-600">
          <CardHeader>
            <CardTitle>Workflow Intelligence Summary</CardTitle>
            <CardDescription>Operational diagnostic results</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="text-sm text-slate-500 mb-1">Maturity Level</div>
                <div className="font-semibold text-lg">{workflow.intelligence.workflow_maturity}</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="text-sm text-slate-500 mb-1">Risk Level</div>
                <div className="font-semibold text-lg">{workflow.intelligence.workflow_risk_level}</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg col-span-2">
                <div className="text-sm text-slate-500 mb-1">Critical Bottleneck</div>
                <div className="font-semibold">{workflow.intelligence.executive_summary.most_critical_bottleneck}</div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-medium border-b pb-2">Identified Bottlenecks</h3>
              {workflow.intelligence.bottlenecks.map((b: any, idx: number) => (
                <div key={idx} className="p-4 border rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold">{b.title}</h4>
                    <Badge variant={b.severity === 'Critical' ? 'destructive' : 'default'}>{b.severity}</Badge>
                  </div>
                  <p className="text-sm text-slate-600 mb-2">{b.rationale}</p>
                  <div className="bg-slate-50 p-3 rounded text-sm">
                    <strong>Root Cause:</strong> {b.root_cause.root_cause}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

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
                  <div key={idx} className="flex justify-between items-center p-4 border rounded-lg shadow-sm" style={{ background: 'var(--tx-bg-card)' }}>
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
