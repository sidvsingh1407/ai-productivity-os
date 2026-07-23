import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { engineeringApi, EngineeringRecordCreate, Consultant } from '@/api/engineering';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';

export default function EngineeringSettings() {
  const queryClient = useQueryClient();

  // Load existing if available
  const { data: records, isLoading } = useQuery({
    queryKey: ['engineering-records'],
    queryFn: engineeringApi.list,
  });

  const existingRecord = records?.[0];

  const createMutation = useMutation({
    mutationFn: engineeringApi.create,
    onSuccess: () => {
      toast.success('Engineering Intelligence updated successfully.');
      queryClient.invalidateQueries({ queryKey: ['engineering-records'] });
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Failed to update Engineering Intelligence');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: any) => engineeringApi.update(existingRecord!.id, data),
    onSuccess: () => {
      toast.success('Engineering Intelligence updated successfully.');
      queryClient.invalidateQueries({ queryKey: ['engineering-records'] });
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Failed to update Engineering Intelligence');
    },
  });

  const [formData, setFormData] = useState({
    has_dedicated_ai_team: 'false',
    team_size: '0',
    roles: '', // comma separated
    has_mlops_pipeline: 'false',
    monitoring_tooling: '', // comma separated
    has_dedicated_prompt_engineer: 'false',
    prompt_engineer_count: '0',
    has_dedicated_devops: 'false',
    devops_support_type: 'not_specified',
    ai_engineering_budget: '',
    planned_investment_roadmap: '',
  });

  const [consultants, setConsultants] = useState<Consultant[]>([]);

  useEffect(() => {
    if (existingRecord) {
      setFormData({
        has_dedicated_ai_team: existingRecord.has_dedicated_ai_team ? 'true' : 'false',
        team_size: existingRecord.team_size.toString(),
        roles: existingRecord.roles.join(', '),
        has_mlops_pipeline: existingRecord.has_mlops_pipeline ? 'true' : 'false',
        monitoring_tooling: existingRecord.monitoring_tooling.join(', '),
        has_dedicated_prompt_engineer: existingRecord.has_dedicated_prompt_engineer ? 'true' : 'false',
        prompt_engineer_count: existingRecord.prompt_engineer_count.toString(),
        has_dedicated_devops: existingRecord.has_dedicated_devops ? 'true' : 'false',
        devops_support_type: existingRecord.devops_support_type,
        ai_engineering_budget: existingRecord.ai_engineering_budget ? existingRecord.ai_engineering_budget.toString() : '',
        planned_investment_roadmap: existingRecord.planned_investment_roadmap || '',
      });
      setConsultants(existingRecord.consultants_used || []);
    }
  }, [existingRecord]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleAddConsultant = () => {
    setConsultants(prev => [...prev, { vendor: '', engagement: '' }]);
  };

  const handleConsultantChange = (index: number, field: keyof Consultant, value: string) => {
    const updated = [...consultants];
    updated[index][field] = value;
    setConsultants(updated);
  };

  const handleRemoveConsultant = (index: number) => {
    setConsultants(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const payload: EngineeringRecordCreate = {
      has_dedicated_ai_team: formData.has_dedicated_ai_team === 'true',
      team_size: parseInt(formData.team_size) || 0,
      roles: formData.roles.split(',').map(r => r.trim()).filter(r => r),
      consultants_used: consultants,
      has_mlops_pipeline: formData.has_mlops_pipeline === 'true',
      monitoring_tooling: formData.monitoring_tooling.split(',').map(r => r.trim()).filter(r => r),
      has_dedicated_prompt_engineer: formData.has_dedicated_prompt_engineer === 'true',
      prompt_engineer_count: parseInt(formData.prompt_engineer_count) || 0,
      has_dedicated_devops: formData.has_dedicated_devops === 'true',
      devops_support_type: formData.devops_support_type,
      ai_engineering_budget: formData.ai_engineering_budget ? parseFloat(formData.ai_engineering_budget) : null,
      planned_investment_roadmap: formData.planned_investment_roadmap || null,
    };

    if (existingRecord) {
      updateMutation.mutate(payload);
    } else {
      createMutation.mutate(payload);
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center text-slate-500">Loading Engineering Intelligence...</div>;
  }

  const isPending = createMutation.isPending || updateMutation.isPending;

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Engineering Intelligence</h1>
        <p className="text-sm text-slate-500">Track internal AI capabilities, tooling, and engineering resources.</p>

        {existingRecord && (
          <div className="mt-4 inline-block px-3 py-1 rounded bg-blue-50 border border-blue-100">
            <span className="text-sm font-medium text-blue-800">
              Current Engineering Score: {existingRecord.engineering_score}/100
            </span>
          </div>
        )}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Engineering Readiness</CardTitle>
          <CardDescription>Details about your AI teams and operations.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label>Has Dedicated AI Team</Label>
                <Select name="has_dedicated_ai_team" value={formData.has_dedicated_ai_team} onChange={handleChange as any} options={[{value: 'false', label: 'No'}, {value: 'true', label: 'Yes'}]} />
              </div>

              <div className="space-y-2">
                <Label>Team Size</Label>
                <Input type="number" name="team_size" min="0" value={formData.team_size} onChange={handleChange} />
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label>Roles Present (Comma-separated)</Label>
                <Input name="roles" placeholder="e.g. Data Scientist, ML Engineer, Prompt Engineer" value={formData.roles} onChange={handleChange} />
              </div>

              <div className="space-y-2 md:col-span-2 border-t pt-4">
                <Label className="flex justify-between items-center">
                  Consultants / External Vendors
                  <Button type="button" variant="outline" size="sm" onClick={handleAddConsultant}>Add Consultant</Button>
                </Label>
                {consultants.map((consultant, idx) => (
                  <div key={idx} className="flex gap-2 items-start mt-2">
                    <Input placeholder="Vendor Name" value={consultant.vendor} onChange={e => handleConsultantChange(idx, 'vendor', e.target.value)} />
                    <Input placeholder="Engagement Type" value={consultant.engagement} onChange={e => handleConsultantChange(idx, 'engagement', e.target.value)} />
                    <Button type="button" variant="ghost" onClick={() => handleRemoveConsultant(idx)} className="text-red-500">Remove</Button>
                  </div>
                ))}
                {consultants.length === 0 && <p className="text-sm text-slate-500 mt-2">No consultants added.</p>}
              </div>

              <div className="space-y-2 border-t pt-4">
                <Label>Has MLOps Pipeline</Label>
                <Select name="has_mlops_pipeline" value={formData.has_mlops_pipeline} onChange={handleChange as any} options={[{value: 'false', label: 'No'}, {value: 'true', label: 'Yes'}]} />
              </div>

              <div className="space-y-2 border-t pt-4">
                <Label>Monitoring Tooling (Comma-separated)</Label>
                <Input name="monitoring_tooling" placeholder="e.g. Prometheus, Grafana, Datadog" value={formData.monitoring_tooling} onChange={handleChange} />
              </div>

              <div className="space-y-2">
                <Label>Has Dedicated Prompt Engineer</Label>
                <Select name="has_dedicated_prompt_engineer" value={formData.has_dedicated_prompt_engineer} onChange={handleChange as any} options={[{value: 'false', label: 'No'}, {value: 'true', label: 'Yes'}]} />
              </div>

              <div className="space-y-2">
                <Label>Prompt Engineer Count</Label>
                <Input type="number" name="prompt_engineer_count" min="0" value={formData.prompt_engineer_count} onChange={handleChange} />
              </div>

              <div className="space-y-2">
                <Label>Has Dedicated DevOps for AI</Label>
                <Select name="has_dedicated_devops" value={formData.has_dedicated_devops} onChange={handleChange as any} options={[{value: 'false', label: 'No'}, {value: 'true', label: 'Yes'}]} />
              </div>

              <div className="space-y-2">
                <Label>DevOps Support Type</Label>
                <Select name="devops_support_type" value={formData.devops_support_type} onChange={handleChange as any} options={[{value: 'not_specified', label: 'Not Specified'}, {value: 'shared', label: 'Shared'}, {value: 'dedicated', label: 'Dedicated'}]} />
              </div>

              <div className="space-y-2 border-t pt-4">
                <Label>AI Engineering Budget (USD)</Label>
                <Input type="number" name="ai_engineering_budget" step="0.01" min="0" value={formData.ai_engineering_budget} onChange={handleChange} />
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label>Planned Investment / Roadmap</Label>
                <Textarea name="planned_investment_roadmap" rows={3} value={formData.planned_investment_roadmap} onChange={handleChange} />
              </div>

            </div>

            <div className="flex justify-end pt-4">
              <Button type="submit" disabled={isPending}>
                {isPending ? 'Saving...' : 'Save Engineering Intelligence'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}