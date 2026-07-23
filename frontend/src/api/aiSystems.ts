import apiClient from './client';

export interface AISystem {
  id: string;
  name: string;
  purpose?: string;
  data_types: string[];
  decision_making_role: string;
  status: 'active' | 'inactive' | 'archived';
  organization_id: string;
  created_at: string;
  updated_at: string;

  version?: string;
  lifecycle_status?: string;
  owner?: string;
  department?: string;
  business_capability?: string;
  internal_external_users?: string;
  criticality?: string;
  implementation_stage?: string;
  ai_type?: string;
  vendor?: string;
  model_name?: string;
  model_version?: string;
  api_provider?: string;
  framework?: string;
  hosting?: string;
  integrations?: string[];
  authentication_method?: string;
  vector_db?: string;
  knowledge_sources?: string[];
  workflow_engine?: string;
  agent_framework?: string;
  deployment_type?: string;
  data_flow?: string;
  apis?: string[];
  databases?: string[];
  event_systems?: string;
  caching?: string;
  monitoring?: string;
  logging?: string;
  deployment_details?: string;
  data_sensitivity?: string;
  data_sources?: string[];
  data_destinations?: string[];
  data_quality_notes?: string;
  data_owner?: string;
  data_freshness?: string;
  data_accessibility?: string[];
  data_availability?: string;
  usage_frequency?: string;
  users_count?: number;
  uptime?: number;
  approvals_required?: boolean;
  risk_classification?: string;
  oversight_status?: string;
  documentation_status?: string;
  applicable_policies?: string[];
  rbac_enabled?: boolean;
  encryption_status?: string;
  incident_count?: number;
}

export type AISystemCreate = Omit<AISystem, 'id' | 'organization_id' | 'created_at' | 'updated_at'>;
export type AISystemUpdate = Partial<AISystemCreate>;

export const aiSystemsApi = {
  list: async (): Promise<AISystem[]> => {
    const { data } = await apiClient.get('/api/ai-systems', {
      params: { limit: 200, offset: 0 }
    });
    return data;
  },

  get: async (id: string): Promise<AISystem> => {
    const { data } = await apiClient.get(`/api/ai-systems/${id}`);
    return data;
  },

  create: async (payload: AISystemCreate): Promise<AISystem> => {
    const { data } = await apiClient.post('/api/ai-systems', payload);
    return data;
  },

  update: async (id: string, payload: AISystemUpdate): Promise<AISystem> => {
    const { data } = await apiClient.put(`/api/ai-systems/${id}`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/ai-systems/${id}`);
  }
};
