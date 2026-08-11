import apiClient from './client';

export interface OrgCostData {
  total: number;
  is_partial: boolean;
  systems_with_data: number;
  total_systems: number;
}

export interface FinancialIntelligenceResponse {
  org_cost: OrgCostData;
  cost_by_criticality: Record<string, OrgCostData>;
}

export const organizationsApi = {
  getFinancialIntelligence: async (): Promise<FinancialIntelligenceResponse> => {
    const response = await apiClient.get('/organizations/me/financial-intelligence');
    return response.data;
  },
};
