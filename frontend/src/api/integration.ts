import apiClient from './client';

export const integrationApi = {
  listIntegrations: async () => {
    const response = await apiClient.get('/integrations');
    return response.data;
  },
  connectIntegration: async (data: any) => {
    const response = await apiClient.post('/integrations/connect', data);
    return response.data;
  },
};
