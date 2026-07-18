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
