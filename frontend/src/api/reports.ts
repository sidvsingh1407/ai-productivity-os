import apiClient from './client';

export const reportsApi = {
  generateReport: async (data: any) => {
    const response = await apiClient.post('/reports/generate', data);
    return response.data;
  },
  listReports: async () => {
    const response = await apiClient.get('/reports');
    return response.data;
  },
};
