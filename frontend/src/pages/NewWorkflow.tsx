import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { ArrowRight, Loader2, Plus, Trash2 } from 'lucide-react';

interface DiagnosticStepInput {
  step_name: string;
  owner_role: string;
  requires_approval: string;
  system_tool: string;
  manual_handoff: string;
}

export default function NewWorkflow() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const sourceAuditId = searchParams.get('auditId');

  const [workflowName, setWorkflowName] = useState('');
  const [steps, setSteps] = useState<DiagnosticStepInput[]>([{
    step_name: '',
    owner_role: '',
    requires_approval: 'false',
    system_tool: '',
    manual_handoff: 'false'
  }]);

  const parseBoolean = (val: string) => val === 'true';
  const parseString = (val: string) => val === '' ? undefined : val;

  const handleStepChange = (index: number, field: keyof DiagnosticStepInput, value: string) => {
    const newSteps = [...steps];
    newSteps[index][field] = value;
    setSteps(newSteps);
  };

  const addStep = () => {
    setSteps([...steps, {
      step_name: '',
      owner_role: '',
      requires_approval: 'false',
      system_tool: '',
      manual_handoff: 'false'
    }]);
  };

  const removeStep = (index: number) => {
    if (steps.length > 1) {
      setSteps(steps.filter((_, i) => i !== index));
    }
  };

  const workflowMutation = useMutation({
    mutationFn: async () => {
      const input_config = {
        mode: 'diagnostic',
        source_audit_id: sourceAuditId || undefined,
        workflow_name: workflowName
      };

      const steps_input = steps.map(step => ({
        step_name: step.step_name,
        owner_role: step.owner_role,
        requires_approval: parseBoolean(step.requires_approval),
        system_tool: parseString(step.system_tool),
        manual_handoff: parseBoolean(step.manual_handoff)
      }));

      const response = await apiClient.post('/workflows/', { input_config, steps_input });
      return response.data;
    },
    onSuccess: (data) => {
      navigate(`/app/workflows/${data.id}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    workflowMutation.mutate();
  };

  return (
    <div className="max-w-3xl mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Run Workflow Intelligence</h1>
        <p className="text-slate-500 mt-2">
          Describe your operational workflow to generate automation blueprints and diagnostics.
          {sourceAuditId && <span className="block mt-1 font-medium text-primary">Linked to Audit ID: {sourceAuditId}</span>}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Workflow Details</CardTitle>
            <CardDescription>Name your workflow to track it in diagnostics.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Label htmlFor="workflowName">Workflow Name *</Label>
              <Input
                id="workflowName"
                name="workflowName"
                placeholder="e.g. Employee Onboarding Process"
                value={workflowName}
                onChange={(e) => setWorkflowName(e.target.value)}
                required
              />
            </div>
          </CardContent>
        </Card>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-slate-900">Workflow Steps</h2>
          {steps.map((step, index) => (
            <Card key={index} className="relative">
              <CardHeader className="pb-4">
                <div className="flex justify-between items-center">
                  <CardTitle className="text-lg">Step {index + 1}</CardTitle>
                  {steps.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => removeStep(index)}
                      className="text-red-500 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Remove
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor={`step_name_${index}`}>Step Name *</Label>
                    <Input
                      id={`step_name_${index}`}
                      placeholder="e.g. Review Application"
                      value={step.step_name}
                      onChange={(e) => handleStepChange(index, 'step_name', e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`owner_role_${index}`}>Owner Role *</Label>
                    <Input
                      id={`owner_role_${index}`}
                      placeholder="e.g. HR Manager"
                      value={step.owner_role}
                      onChange={(e) => handleStepChange(index, 'owner_role', e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`system_tool_${index}`}>System Tool</Label>
                    <Input
                      id={`system_tool_${index}`}
                      placeholder="e.g. Jira, Workday"
                      value={step.system_tool}
                      onChange={(e) => handleStepChange(index, 'system_tool', e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`requires_approval_${index}`}>Requires Approval</Label>
                    <Select
                      id={`requires_approval_${index}`}
                      value={step.requires_approval}
                      onChange={(e) => handleStepChange(index, 'requires_approval', e.target.value)}
                      options={[
                        { value: 'true', label: 'Yes' },
                        { value: 'false', label: 'No' },
                      ]}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`manual_handoff_${index}`}>Manual Handoff</Label>
                    <Select
                      id={`manual_handoff_${index}`}
                      value={step.manual_handoff}
                      onChange={(e) => handleStepChange(index, 'manual_handoff', e.target.value)}
                      options={[
                        { value: 'true', label: 'Yes' },
                        { value: 'false', label: 'No' },
                      ]}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="flex justify-between items-center border-t pt-6">
          <Button type="button" variant="outline" onClick={addStep}>
            <Plus className="mr-2 h-4 w-4" />
            Add Step
          </Button>

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
    </div>
  );
}
