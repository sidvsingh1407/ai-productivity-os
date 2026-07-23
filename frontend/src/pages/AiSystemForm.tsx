import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { aiSystemsApi, AISystemCreate, AISystemUpdate } from '@/api/aiSystems';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
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
    data_types: '', // Comma-separated string
    decision_making_role: '',
    status: 'active',

    // Identity
    version: '',
    owner: '',
    department: '',

    // Business
    business_capability: '',
    internal_external_users: '',
    criticality: '',
    implementation_stage: '',
    vendor: '',

    // Technology
    ai_type: '',
    model_name: '',
    model_version: '',
    api_provider: '',
    framework: '',
    vector_db: '',
    agent_framework: '',

    // Architecture
    hosting: '',
    integrations: '', // Comma-separated string
    workflow_engine: '',
    deployment_type: '',
    data_flow: '',
    apis: '', // Comma-separated string
    databases: '', // Comma-separated string
    event_systems: '',
    caching: '',
    deployment_details: '',

    // Data
    knowledge_sources: '', // Comma-separated string
    data_sensitivity: '',
    data_sources: '', // Comma-separated string
    data_destinations: '', // Comma-separated string
    data_quality_notes: '',
    data_owner: '',
    data_freshness: '',
    data_accessibility: '', // Comma-separated string
    data_availability: '',

    // Operations
    lifecycle_status: '',
    usage_frequency: '',
    users_count: '', // Number as string for form
    uptime: '', // Number as string for form
    monitoring: '',
    logging: '',
    incident_count: '', // Number as string for form

    // Governance
    approvals_required: 'false', // boolean as string
    risk_classification: '',
    oversight_status: '',
    documentation_status: '',

    // Security
    authentication_method: '',
    rbac_enabled: 'false', // boolean as string
    encryption_status: '',

    // Compliance
    applicable_policies: '', // Comma-separated string
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

        version: existingSystem.version || '',
        owner: existingSystem.owner || '',
        department: existingSystem.department || '',

        business_capability: existingSystem.business_capability || '',
        internal_external_users: existingSystem.internal_external_users || '',
        criticality: existingSystem.criticality || '',
        implementation_stage: existingSystem.implementation_stage || '',
        vendor: existingSystem.vendor || '',

        ai_type: existingSystem.ai_type || '',
        model_name: existingSystem.model_name || '',
        model_version: existingSystem.model_version || '',
        api_provider: existingSystem.api_provider || '',
        framework: existingSystem.framework || '',
        vector_db: existingSystem.vector_db || '',
        agent_framework: existingSystem.agent_framework || '',

        hosting: existingSystem.hosting || '',
        integrations: existingSystem.integrations ? existingSystem.integrations.join(', ') : '',
        workflow_engine: existingSystem.workflow_engine || '',
        deployment_type: existingSystem.deployment_type || '',
        data_flow: existingSystem.data_flow || '',
        apis: existingSystem.apis ? existingSystem.apis.join(', ') : '',
        databases: existingSystem.databases ? existingSystem.databases.join(', ') : '',
        event_systems: existingSystem.event_systems || '',
        caching: existingSystem.caching || '',
        deployment_details: existingSystem.deployment_details || '',

        knowledge_sources: existingSystem.knowledge_sources ? existingSystem.knowledge_sources.join(', ') : '',
        data_sensitivity: existingSystem.data_sensitivity || '',
        data_sources: existingSystem.data_sources ? existingSystem.data_sources.join(', ') : '',
        data_destinations: existingSystem.data_destinations ? existingSystem.data_destinations.join(', ') : '',
        data_quality_notes: existingSystem.data_quality_notes || '',
        data_owner: existingSystem.data_owner || '',
        data_freshness: existingSystem.data_freshness || '',
        data_accessibility: existingSystem.data_accessibility ? existingSystem.data_accessibility.join(', ') : '',
        data_availability: existingSystem.data_availability || '',

        lifecycle_status: existingSystem.lifecycle_status || '',
        usage_frequency: existingSystem.usage_frequency || '',
        users_count: existingSystem.users_count !== undefined ? String(existingSystem.users_count) : '',
        uptime: existingSystem.uptime !== undefined ? String(existingSystem.uptime) : '',
        monitoring: existingSystem.monitoring || '',
        logging: existingSystem.logging || '',
        incident_count: existingSystem.incident_count !== undefined ? String(existingSystem.incident_count) : '0',

        approvals_required: existingSystem.approvals_required !== undefined ? String(existingSystem.approvals_required) : 'false',
        risk_classification: existingSystem.risk_classification || '',
        oversight_status: existingSystem.oversight_status || '',
        documentation_status: existingSystem.documentation_status || '',

        authentication_method: existingSystem.authentication_method || '',
        rbac_enabled: existingSystem.rbac_enabled !== undefined ? String(existingSystem.rbac_enabled) : 'false',
        encryption_status: existingSystem.encryption_status || '',

        applicable_policies: existingSystem.applicable_policies ? existingSystem.applicable_policies.join(', ') : '',
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

  const parseCommaSeparated = (str: string) => {
    return str
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0);
  };

  const parseNumber = (val: string) => val === '' ? undefined : Number(val);
  const parseBoolean = (val: string) => val === 'true';
  const parseString = (val: string) => val === '' ? undefined : val;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const payload: AISystemCreate = {
      name: formData.name,
      purpose: parseString(formData.purpose),
      data_types: parseCommaSeparated(formData.data_types),
      decision_making_role: formData.decision_making_role,
      status: formData.status as 'active' | 'inactive' | 'archived',

      version: parseString(formData.version),
      owner: parseString(formData.owner),
      department: parseString(formData.department),

      business_capability: parseString(formData.business_capability),
      internal_external_users: parseString(formData.internal_external_users),
      criticality: parseString(formData.criticality),
      implementation_stage: parseString(formData.implementation_stage),
      vendor: parseString(formData.vendor),

      ai_type: parseString(formData.ai_type),
      model_name: parseString(formData.model_name),
      model_version: parseString(formData.model_version),
      api_provider: parseString(formData.api_provider),
      framework: parseString(formData.framework),
      vector_db: parseString(formData.vector_db),
      agent_framework: parseString(formData.agent_framework),

      hosting: parseString(formData.hosting),
      integrations: parseCommaSeparated(formData.integrations),
      workflow_engine: parseString(formData.workflow_engine),
      deployment_type: parseString(formData.deployment_type),
      data_flow: parseString(formData.data_flow),
      apis: parseCommaSeparated(formData.apis),
      databases: parseCommaSeparated(formData.databases),
      event_systems: parseString(formData.event_systems),
      caching: parseString(formData.caching),
      deployment_details: parseString(formData.deployment_details),

      knowledge_sources: parseCommaSeparated(formData.knowledge_sources),
      data_sensitivity: parseString(formData.data_sensitivity),
      data_sources: parseCommaSeparated(formData.data_sources),
      data_destinations: parseCommaSeparated(formData.data_destinations),
      data_quality_notes: parseString(formData.data_quality_notes),
      data_owner: parseString(formData.data_owner),
      data_freshness: parseString(formData.data_freshness),
      data_accessibility: parseCommaSeparated(formData.data_accessibility),
      data_availability: parseString(formData.data_availability),

      lifecycle_status: parseString(formData.lifecycle_status),
      usage_frequency: parseString(formData.usage_frequency),
      users_count: parseNumber(formData.users_count),
      uptime: parseNumber(formData.uptime),
      monitoring: parseString(formData.monitoring),
      logging: parseString(formData.logging),
      incident_count: parseNumber(formData.incident_count),

      approvals_required: parseBoolean(formData.approvals_required),
      risk_classification: parseString(formData.risk_classification),
      oversight_status: parseString(formData.oversight_status),
      documentation_status: parseString(formData.documentation_status),

      authentication_method: parseString(formData.authentication_method),
      rbac_enabled: parseBoolean(formData.rbac_enabled),
      encryption_status: parseString(formData.encryption_status),

      applicable_policies: parseCommaSeparated(formData.applicable_policies),
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

  const renderInput = (id: string, label: string, placeholder?: string, type: string = "text", required: boolean = false) => (
    <div className="space-y-2">
      <Label htmlFor={id}>{label} {required && '*'}</Label>
      <Input
        id={id}
        name={id}
        type={type}
        placeholder={placeholder}
        value={(formData as any)[id]}
        onChange={handleChange}
        required={required}
      />
    </div>
  );

  const renderTextarea = (id: string, label: string, placeholder?: string, required: boolean = false) => (
    <div className="space-y-2">
      <Label htmlFor={id}>{label} {required && '*'}</Label>
      <Textarea
        id={id}
        name={id}
        placeholder={placeholder}
        value={(formData as any)[id]}
        onChange={handleChange}
        required={required}
        className="min-h-[100px]"
      />
    </div>
  );

  const renderCommaSeparated = (id: string, label: string, placeholder?: string) => (
    <div className="space-y-2 md:col-span-2">
      <Label htmlFor={id}>{label}</Label>
      <Input
        id={id}
        name={id}
        placeholder={placeholder || "Enter comma-separated values."}
        value={(formData as any)[id]}
        onChange={handleChange}
      />
      <p className="text-xs text-slate-500">Enter comma-separated values.</p>
    </div>
  );

  const renderSelect = (id: string, label: string, options: {value: string, label: string}[], required: boolean = false) => (
    <div className="space-y-2">
      <Label htmlFor={id}>{label} {required && '*'}</Label>
      <Select
        id={id}
        name={id}
        value={(formData as any)[id]}
        onChange={handleChange}
        options={options}
        required={required}
      />
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto py-8">
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

            <Tabs defaultValue="identity" className="w-full">
              <TabsList className="flex flex-wrap h-auto mb-6">
                <TabsTrigger value="identity">Identity</TabsTrigger>
                <TabsTrigger value="business">Business</TabsTrigger>
                <TabsTrigger value="technology">Technology</TabsTrigger>
                <TabsTrigger value="architecture">Architecture</TabsTrigger>
                <TabsTrigger value="data">Data</TabsTrigger>
                <TabsTrigger value="operations">Operations</TabsTrigger>
                <TabsTrigger value="governance">Governance</TabsTrigger>
                <TabsTrigger value="security">Security</TabsTrigger>
                <TabsTrigger value="compliance">Compliance</TabsTrigger>
              </TabsList>

              <TabsContent value="identity" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderInput('name', 'System Name', 'e.g. Customer Support Bot', 'text', true)}
                  {renderInput('version', 'Version', 'e.g. 1.0.0')}
                  {renderInput('owner', 'Owner', 'e.g. John Doe')}
                  {renderInput('department', 'Department', 'e.g. Engineering')}
                </div>
              </TabsContent>

              <TabsContent value="business" className="space-y-4">
                {renderTextarea('purpose', 'Purpose', 'Describe the primary purpose of this AI system...')}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderInput('business_capability', 'Business Capability')}
                  {renderInput('internal_external_users', 'Internal/External Users')}
                  {renderInput('criticality', 'Criticality')}
                  {renderInput('implementation_stage', 'Implementation Stage')}
                  {renderInput('vendor', 'Vendor')}
                </div>
              </TabsContent>

              <TabsContent value="technology" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderInput('ai_type', 'AI Type')}
                  {renderInput('model_name', 'Model Name')}
                  {renderInput('model_version', 'Model Version')}
                  {renderInput('api_provider', 'API Provider')}
                  {renderInput('framework', 'Framework')}
                  {renderInput('vector_db', 'Vector DB')}
                  {renderInput('agent_framework', 'Agent Framework')}
                </div>
              </TabsContent>

              <TabsContent value="architecture" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderInput('hosting', 'Hosting')}
                  {renderInput('workflow_engine', 'Workflow Engine')}
                  {renderInput('deployment_type', 'Deployment Type')}
                  {renderInput('data_flow', 'Data Flow')}
                  {renderInput('event_systems', 'Event Systems')}
                  {renderInput('caching', 'Caching')}
                  {renderInput('deployment_details', 'Deployment Details')}
                  {renderCommaSeparated('integrations', 'Integrations')}
                  {renderCommaSeparated('apis', 'APIs')}
                  {renderCommaSeparated('databases', 'Databases')}
                </div>
              </TabsContent>

              <TabsContent value="data" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderCommaSeparated('data_types', 'Data Types')}
                  {renderCommaSeparated('knowledge_sources', 'Knowledge Sources')}
                  {renderInput('data_sensitivity', 'Data Sensitivity')}
                  {renderCommaSeparated('data_sources', 'Data Sources')}
                  {renderCommaSeparated('data_destinations', 'Data Destinations')}

                  {renderInput('data_quality_notes', 'Data Quality Notes')}
                  {renderInput('data_owner', 'Data Owner')}
                  {renderSelect('data_freshness', 'Data Freshness', [
                    { value: '', label: 'Select Freshness...' },
                    { value: 'real_time', label: 'Real Time' },
                    { value: 'daily', label: 'Daily' },
                    { value: 'weekly', label: 'Weekly' },
                    { value: 'monthly', label: 'Monthly' },
                    { value: 'static', label: 'Static' },
                    { value: 'unknown', label: 'Unknown' },
                  ])}
                  {renderCommaSeparated('data_accessibility', 'Data Accessibility')}
                  {renderInput('data_availability', 'Data Availability')}
                </div>
              </TabsContent>

              <TabsContent value="operations" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderSelect('status', 'Status', [
                    { value: 'active', label: 'Active' },
                    { value: 'inactive', label: 'Inactive' },
                    { value: 'archived', label: 'Archived' },
                  ], true)}
                  {renderInput('lifecycle_status', 'Lifecycle Status')}
                  {renderInput('usage_frequency', 'Usage Frequency')}
                  {renderInput('users_count', 'Users Count', '', 'number')}
                  {renderInput('uptime', 'Uptime', '', 'number')}
                  {renderInput('monitoring', 'Monitoring')}
                  {renderInput('logging', 'Logging')}
                  {renderInput('incident_count', 'Incident Count', '', 'number')}
                </div>
              </TabsContent>

              <TabsContent value="governance" className="space-y-4">
                {renderTextarea('decision_making_role', 'Decision Making Role', 'How does this system participate in decision-making? (e.g. advisory, automated)', true)}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderSelect('approvals_required', 'Approvals Required', [
                    { value: 'true', label: 'Yes' },
                    { value: 'false', label: 'No' },
                  ])}
                  {renderInput('risk_classification', 'Risk Classification')}
                  {renderInput('oversight_status', 'Oversight Status')}
                  {renderInput('documentation_status', 'Documentation Status')}
                </div>
              </TabsContent>

              <TabsContent value="security" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderInput('authentication_method', 'Authentication Method')}
                  {renderSelect('rbac_enabled', 'RBAC Enabled', [
                    { value: 'true', label: 'Yes' },
                    { value: 'false', label: 'No' },
                  ])}
                  {renderInput('encryption_status', 'Encryption Status')}
                </div>
              </TabsContent>

              <TabsContent value="compliance" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {renderCommaSeparated('applicable_policies', 'Applicable Policies')}
                </div>
              </TabsContent>

            </Tabs>

            <div className="flex justify-end gap-4 mt-8">
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
