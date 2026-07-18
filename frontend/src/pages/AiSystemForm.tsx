import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { aiSystemsApi, AISystemCreate, AISystemUpdate } from '@/api/aiSystems';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select } from '@/components/ui/select';
import { ArrowRight, Loader2, Save } from 'lucide-react';
import { toast } from 'sonner';

export default function AiSystemForm() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEditMode = Boolean(id);
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    name: '',
    purpose: '',
    data_types: '', // We'll manage this as a comma-separated string in the form state
    decision_making_role: '',
    status: 'active',
  });

  const { data: existingSystem, isLoading: isFetching } = useQuery({
    queryKey: ['ai-systems', id],
    queryFn: () => aiSystemsApi.get(id!),
    enabled: isEditMode,
  });

  useEffect(() => {
    if (existingSystem) {
      setFormData({
        name: existingSystem.name || '',
        purpose: existingSystem.purpose || '',
        data_types: existingSystem.data_types ? existingSystem.data_types.join(', ') : '',
        decision_making_role: existingSystem.decision_making_role || '',
        status: existingSystem.status || 'active',
      });
    }
  }, [existingSystem]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const createMutation = useMutation({
    mutationFn: (data: AISystemCreate) => aiSystemsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai-systems'] });
      toast.success('AI System created successfully');
      navigate('/app/ai-systems');
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail || 'Failed to create AI system');
    }
  });

  const updateMutation = useMutation({
    mutationFn: (data: AISystemUpdate) => aiSystemsApi.update(id!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai-systems'] });
      queryClient.invalidateQueries({ queryKey: ['ai-systems', id] });
      toast.success('AI System updated successfully');
      navigate('/app/ai-systems');
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail || 'Failed to update AI system');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Parse data_types string into an array
    const dataTypesArray = formData.data_types
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0);

    const payload = {
      ...formData,
      status: formData.status as 'active' | 'inactive' | 'archived',
      data_types: dataTypesArray,
    };

    if (isEditMode) {
      updateMutation.mutate(payload);
    } else {
      createMutation.mutate(payload);
    }
  };

  const isPending = createMutation.isPending || updateMutation.isPending;

  if (isEditMode && isFetching) {
    return <div className="p-8 text-center text-slate-500">Loading system details...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">
          {isEditMode ? 'Edit AI System' : 'Register AI System'}
        </h1>
        <p className="text-slate-500 mt-2">
          {isEditMode
            ? 'Update the details of this AI system.'
            : 'Register a new AI system in your organization inventory.'}
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>System Details</CardTitle>
          <CardDescription>Fill out the form below to {isEditMode ? 'update' : 'create'} the system.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="name">System Name *</Label>
                <Input
                  id="name"
                  name="name"
                  placeholder="e.g. Customer Support Bot"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  options={[
                    { value: 'active', label: 'Active' },
                    { value: 'inactive', label: 'Inactive' },
                    { value: 'archived', label: 'Archived' },
                  ]}
                  required
                />
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="data_types">Data Types</Label>
                <Input
                  id="data_types"
                  name="data_types"
                  placeholder="e.g. PII, Financial, Health (comma-separated)"
                  value={formData.data_types}
                  onChange={handleChange}
                />
                <p className="text-xs text-slate-500">Enter comma-separated values.</p>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="purpose">Purpose</Label>
              <Textarea
                id="purpose"
                name="purpose"
                placeholder="Describe the primary purpose of this AI system..."
                value={formData.purpose}
                onChange={handleChange}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="decision_making_role">Decision Making Role *</Label>
              <Textarea
                id="decision_making_role"
                name="decision_making_role"
                placeholder="How does this system participate in decision-making? (e.g. advisory, automated)"
                value={formData.decision_making_role}
                onChange={handleChange}
                required
                className="min-h-[100px]"
              />
            </div>

            <div className="flex justify-end gap-4">
              <Button type="button" variant="outline" onClick={() => navigate('/app/ai-systems')}>
                Cancel
              </Button>
              <Button type="submit" disabled={isPending}>
                {isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {isEditMode ? 'Updating...' : 'Saving...'}
                  </>
                ) : (
                  <>
                    {isEditMode ? 'Update System' : 'Create System'}
                    {isEditMode ? <Save className="ml-2 h-4 w-4" /> : <ArrowRight className="ml-2 h-4 w-4" />}
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
