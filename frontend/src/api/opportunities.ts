import apiClient from './client';

export interface Opportunity {
  id: string;
  category: string;
  title: string;
  description: string;
  source_module: string;
  confidence_or_priority: string;
  organization_id: string;
  ai_system_id: string | null;
  created_at: string;
}

export interface OpportunityListResponse {
  items: Opportunity[];
  total: number;
  skip: number;
  limit: number;
}

export const opportunitiesApi = {
  list: async (ai_system_id?: string, category?: string): Promise<OpportunityListResponse> => {
    const params = new URLSearchParams();
    if (ai_system_id !== undefined) params.append('ai_system_id', ai_system_id);
    if (category !== undefined) params.append('category', category);

    const response = await apiClient.get<OpportunityListResponse>(`/api/opportunities/?${params.toString()}`);
    return response.data;
  },

  generate: async (): Promise<{ status: string; message: string }> => {
    const response = await apiClient.post<{ status: string; message: string }>('/api/opportunities/generate');
    return response.data;
  }
};
