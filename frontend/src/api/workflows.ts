import apiClient from './client';

export const workflowsApi = {
  createWorkflow: async (data: any) => {
    const response = await apiClient.post('/workflows', data);
    return response.data;
  },
  getWorkflow: async (id: string) => {
    const response = await apiClient.get(`/workflows/${id}`);
    return response.data;
  },
  listWorkflows: async () => {
    const response = await apiClient.get('/workflows');
    return response.data;
  },
};
