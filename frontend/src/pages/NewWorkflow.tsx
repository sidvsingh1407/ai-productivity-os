import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

export default function NewWorkflow() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const defaultAuditId = searchParams.get('auditId') || '';

  const [formData, setFormData] = useState({
    auditId: defaultAuditId,
    mode: 'fixture',
    target_min: '5',
    target_max: '10',
    industry_filter: '',
  });

  const mutation = useMutation({
    mutationFn: async (data: any) => {
      // Depending on API, we might not need auditId here, but often linked
      const response = await apiClient.post('/workflows/', data);
      return response.data;
    },
    onSuccess: (data) => {
      navigate(`/workflows/${data.id}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate({
      mode: formData.mode,
      config: {
        target_min: parseInt(formData.target_min),
        target_max: parseInt(formData.target_max),
        industry_filter: formData.industry_filter || null,
      }
    });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="max-w-2xl mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Run Workflow Diagnostic</CardTitle>
          <CardDescription>Configure parameters for the workflow generation process.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              {defaultAuditId && (
                <div className="bg-slate-50 p-3 rounded-md text-sm text-slate-600 mb-4 border">
                  Linking diagnostic to Audit ID: <span className="font-mono">{defaultAuditId}</span>
                </div>
              )}

              <div>
                <Label htmlFor="mode">Diagnostic Mode</Label>
                <Select
                  id="mode"
                  name="mode"
                  value={formData.mode}
                  onChange={handleChange}
                  options={[
                    { value: 'fixture', label: 'Fixture (Test Data)' },
                    { value: 'live', label: 'Live Generation' },
                  ]}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="target_min">Target Minimum Workflows</Label>
                  <Input
                    id="target_min"
                    name="target_min"
                    type="number"
                    min="1"
                    value={formData.target_min}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <Label htmlFor="target_max">Target Maximum Workflows</Label>
                  <Input
                    id="target_max"
                    name="target_max"
                    type="number"
                    min="1"
                    value={formData.target_max}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="industry_filter">Industry Filter (Optional)</Label>
                <Input
                  id="industry_filter"
                  name="industry_filter"
                  value={formData.industry_filter}
                  onChange={handleChange}
                  placeholder="e.g., Finance, Healthcare"
                />
              </div>
            </div>

            <div className="flex justify-end pt-4 border-t">
              <Button type="submit" disabled={mutation.isPending}>
                {mutation.isPending ? 'Starting...' : 'Start Diagnostic'}
              </Button>
            </div>
            {mutation.isError && <p className="text-red-500 text-sm mt-2">Error starting workflow diagnostic.</p>}
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
