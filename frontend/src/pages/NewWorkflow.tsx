import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select } from '@/components/ui/select';
import { ArrowRight, Loader2 } from 'lucide-react';

export default function NewWorkflow() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const sourceAuditId = searchParams.get('auditId');

  const [formData, setFormData] = useState({
    organizationType: '',
    industry: '',
    department: '',
    workflowCategory: '',
    teamSize: '',
    currentToolsUsed: '',
    workflowDescription: '',
    currentChallenges: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const workflowMutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      // Create flexible input_config schema
      const input_config = {
        mode: 'diagnostic', // Just an indicator
        source_audit_id: sourceAuditId || undefined,
        ...data
      };
      const response = await apiClient.post('/workflows/', { input_config });
      return response.data;
    },
    onSuccess: (data) => {
      navigate(`/workflows/${data.id}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    workflowMutation.mutate(formData);
  };

  return (
    <div className="max-w-3xl mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Run Workflow Diagnostic</h1>
        <p className="text-slate-500 mt-2">
          Describe your operational workflow to generate automation blueprints and diagnostics.
          {sourceAuditId && <span className="block mt-1 font-medium text-primary">Linked to Audit ID: {sourceAuditId}</span>}
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Workflow Details</CardTitle>
          <CardDescription>Fill out the form below to begin the analysis.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="organizationType">Organization Type</Label>
                <Select
                  id="organizationType"
                  name="organizationType"
                  value={formData.organizationType}
                  onChange={handleChange}
                  options={[
                    { value: '', label: 'Select Type' },
                    { value: 'Consulting Firm', label: 'Consulting Firm' },
                    { value: 'Government', label: 'Government' },
                    { value: 'Startup', label: 'Startup' },
                    { value: 'SMB', label: 'SMB' },
                    { value: 'Enterprise', label: 'Enterprise' },
                  ]}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="industry">Industry</Label>
                <Input
                  id="industry"
                  name="industry"
                  placeholder="e.g. Healthcare, Finance"
                  value={formData.industry}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="department">Department</Label>
                <Input
                  id="department"
                  name="department"
                  placeholder="e.g. HR, Operations"
                  value={formData.department}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="workflowCategory">Workflow Category</Label>
                <Input
                  id="workflowCategory"
                  name="workflowCategory"
                  placeholder="e.g. Onboarding, Data Entry"
                  value={formData.workflowCategory}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="teamSize">Team Size</Label>
                <Select
                  id="teamSize"
                  name="teamSize"
                  value={formData.teamSize}
                  onChange={handleChange}
                  options={[
                    { value: '', label: 'Select Size' },
                    { value: '1-10', label: '1-10' },
                    { value: '11-50', label: '11-50' },
                    { value: '51-200', label: '51-200' },
                    { value: '200+', label: '200+' },
                  ]}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="currentToolsUsed">Current Tools Used</Label>
                <Input
                  id="currentToolsUsed"
                  name="currentToolsUsed"
                  placeholder="e.g. Excel, Jira, Salesforce"
                  value={formData.currentToolsUsed}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="workflowDescription">Workflow Description</Label>
              <Textarea
                id="workflowDescription"
                name="workflowDescription"
                placeholder="Describe the steps in your workflow..."
                value={formData.workflowDescription}
                onChange={handleChange}
                required
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="currentChallenges">Current Challenges</Label>
              <Textarea
                id="currentChallenges"
                name="currentChallenges"
                placeholder="What are the main bottlenecks or pain points?"
                value={formData.currentChallenges}
                onChange={handleChange}
                required
                className="min-h-[100px]"
              />
            </div>

            <div className="flex justify-end">
              <Button type="submit" size="lg" disabled={workflowMutation.isPending}>
                {workflowMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing Workflow...
                  </>
                ) : (
                  <>
                    Run Diagnostic
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
