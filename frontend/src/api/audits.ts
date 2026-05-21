import apiClient from './client';

export const auditsApi = {
  createAudit: async (data: any) => {
    const response = await apiClient.post('/audits', data);
    return response.data;
  },
  getAudit: async (id: string) => {
    const response = await apiClient.get(`/audits/${id}`);
    return response.data;
  },
  listAudits: async () => {
    const response = await apiClient.get('/audits');
    return response.data;
  },
};
