import apiClient from './client';

export interface Consultant {
  vendor: string;
  engagement: string;
}

export interface EngineeringRecord {
  id: string;
  organization_id: string;
  has_dedicated_ai_team: boolean;
  team_size: number;
  roles: string[];
  consultants_used: Consultant[];

  has_mlops_pipeline: boolean;
  monitoring_tooling: string[];

  has_dedicated_prompt_engineer: boolean;
  prompt_engineer_count: number;

  has_dedicated_devops: boolean;
  devops_support_type: string;

  ai_engineering_budget: number | null;
  planned_investment_roadmap: string | null;

  created_at: string;
  updated_at: string;
  engineering_score: number;
}

export type EngineeringRecordCreate = Omit<EngineeringRecord, 'id' | 'organization_id' | 'created_at' | 'updated_at' | 'engineering_score'>;
export type EngineeringRecordUpdate = Partial<EngineeringRecordCreate>;

export const engineeringApi = {
  list: async (): Promise<EngineeringRecord[]> => {
    const { data } = await apiClient.get('/engineering-records');
    return data;
  },

  get: async (id: string): Promise<EngineeringRecord> => {
    const { data } = await apiClient.get(`/engineering-records/${id}`);
    return data;
  },

  create: async (payload: EngineeringRecordCreate): Promise<EngineeringRecord> => {
    const { data } = await apiClient.post('/engineering-records', payload);
    return data;
  },

  update: async (id: string, payload: EngineeringRecordUpdate): Promise<EngineeringRecord> => {
    const { data } = await apiClient.put(`/engineering-records/${id}`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/engineering-records/${id}`);
  },
};